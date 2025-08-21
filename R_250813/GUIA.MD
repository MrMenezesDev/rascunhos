# Guia Arquitetônico e de Implementação para um Designer Interativo de Estruturas Hexagonais

## Sumário Executivo

Este documento apresenta um guia arquitetônico e um plano de implementação para uma aplicação web de design e visualização de estruturas baseadas em ladrilhos (tiles) hexagonais. O objetivo: permitir gerar, configurar e interagir com uma grade hexagonal, clicando em um tile para exibir um cubo isométrico e disparar uma interface de seleção de direções que estende conexões até a borda lógica da grade. A proposta privilegia arquitetura limpa, performance e extensibilidade.

## Contexto e Abordagem

O código de referência original estava inacessível. Em vez de replicar algo desconhecido, adotamos uma reconstrução fundamentada em princípios: geometria de grades hexagonais, bibliotecas “headless” e padrões modernos (separação de responsabilidades, fluxo de dados unidirecional). O foco é robustez e clareza futura.

## Estrutura do Documento

1. Fundamentos matemáticos e estruturas de dados
2. Renderização no Canvas HTML5
3. Interatividade (pixel → hex, estado, menu de direções)
4. Funcionalidades centrais (cubo isométrico, prolongamento de barras)
5. Arquitetura modular e recomendações

---

## 1. Fundamentos da Grade Hexagonal

A qualidade dos algoritmos depende de representações geométricas corretas. Esta seção cobre geometria, sistemas de coordenadas, seleção de biblioteca e modelagem do tile.

### 1.1 Geometria Essencial

Orientações possíveis:

- Pointy-top (vértice para cima)
- Flat-top (lado para cima)

Para um hex regular de raio (size) = distância centro → vértice:

| Orientação      | Altura (height) | Largura (width) |
|-----------------|-----------------|-----------------|
| Pointy-top      | 2 × size        | 3 × size        |
| Flat-top        | 3 × size        | 2 × size        |

Coordenadas de cada vértice i (0..5):

```
vx_i = cx + size * cos(θ_i)
vy_i = cy + size * sin(θ_i)
```

Com θ_i em incrementos de 60°. O ângulo inicial depende da orientação (ex.: 30° para pointy-top, 0° para flat-top).

### 1.2 Sistemas de Coordenadas

Principais representações:

1. Offset (row/col com deslocamentos) – intuitivo, porém adiciona condicionais complexas.
2. Cube (q, r, s) com restrição q + r + s = 0 – aritmética simples para vizinhos, distância e interpolação.
3. Axial (q, r) – forma comprimida; s = -q - r recuperável.

**Decisão:** Internamente usar coordenadas cúbicas para algoritmos (distância, linha, vizinhos) e expor axial na API pública/armazenamento. Evita ramificações e simplifica operações como “prolongar barra”.

### 1.3 Biblioteca de Lógica: honeycomb-grid

Critério principal: biblioteca headless que não acople lógica à renderização. `honeycomb-grid` satisfaz: cálculo de vizinhos, conversões e utilitários, mantendo UI e desenho independentes. Evita sobrecarga de libs focadas em diagramação (JointJS) ou visualização estática (oi.hexmap.js).

#### Comparativo Resumido

| Biblioteca       | Foco                         | Dependência de render | Adequação |
|------------------|------------------------------|-----------------------|-----------|
| honeycomb-grid   | Lógica (coords, traversals)  | Nenhuma               | Excelente |
| JointJS          | Diagramação completa (SVG)   | Alta (SVG)            | Excessiva |
| oi.hexmap.js     | Exibir cartogramas HexJSON   | SVG                   | Baixa     |

### 1.4 Modelagem de Dados do Tile

Estrutura sugerida:

```ts
type Connection = {
	direction: string;      // ex: 'ne', 'e', ...
	type?: string;          // futuro: tipo de ligação
	weight?: number;        // custo / peso opcional
};

interface Tile {
	id: string;             // derivado de coords ex.: `q0r1`
	coords: { q: number; r: number };
	hexObject: Hex;         // referência honeycomb
	isSelected: boolean;
	isHovered: boolean;
	isActive: boolean;
	connections: Connection[];
}
```

Chaves de extensibilidade: `connections` parametrizadas, flags de UI separadas, identificador estável.

---

## 2. Renderização no Canvas HTML5

### 2.1 Ambiente

Canvas 2D combina performance + controle de pixels para: highlight dinâmico, picking matemático e integração posterior com buffers off-screen. SVG escalaria mal em grandes grades (milhares de nós DOM).

### 2.2 Função de Desenho de Hexágono

```js
function drawHexagon(ctx, center, size, orientation) {
	ctx.beginPath();
	for (let i = 0; i < 6; i++) {
		const angle = baseAngle(orientation) + i * Math.PI / 3; // 60°
		const x = center.x + size * Math.cos(angle);
		const y = center.y + size * Math.sin(angle);
		i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
	}
	ctx.closePath();
	ctx.fill();
	ctx.stroke();
}
```

Otimização: usar `Path2D` para reutilizar a geometria quando `size` fixo.

### 2.3 Loop de Renderização

Fluxo: `requestAnimationFrame` → consulta estado → redesenha cena completa. Evita lógica de redesenho disparada por eventos, mantém animações suaves e previsibilidade.

### 2.4 Feedback Visual

Exemplo:

```js
grid.forEach(hex => {
	const c = hex.toPoint();
	if (hex.equals(state.activeHex)) ctx.fillStyle = '#3b82f6';
	else if (hex.equals(state.hoveredHex)) ctx.fillStyle = '#93c5fd';
	else ctx.fillStyle = '#9ca3af';
	drawHexagon(ctx, c, SIZE, orientation);
});
```

---

## 3. Interatividade

### 3.1 Conversão Pixel → Hex (O(1))

Processo:

1. Normalizar coordenadas do evento (compensar `getBoundingClientRect`).
2. Aplicar transformação inversa → coordenadas fracionárias axiais/cube.
3. Arredondar com algoritmo `hex_round` (ajuste no eixo de maior erro para manter `q + r + s = 0`).

Biblioteca já provê: `Grid.pointToHex(x, y)`.

Alternativas rejeitadas: busca linear por proximidade, color picking em canvas oculto, `ctx.isPointInPath` iterativo – todas O(N) ou frágeis.

### 3.2 Estado Centralizado

```js
const state = {
	grid,             // instância honeycomb
	hoveredHex: null,
	activeHex: null,
	contextMenu: { visible: false, x: 0, y: 0 },
	pendingLine: null // { startHex, direction }
};
```

Handlers disparam mutações controladas; renderer observa e redesenha.

### 3.3 Menu de Direções (Contexto Customizado)

Passos:

1. `<div>` absoluto oculto (CSS `display: none`).
2. Capturar `contextmenu` ou `click` → `preventDefault()`.
3. Posicionar usando coordenadas do evento.
4. Preencher botões (6 direções); cliques geram ação e ocultam menu.
5. Listener global fecha ao clicar fora.

Desafio: alinhar coordenadas DOM ↔ canvas (usar `getBoundingClientRect()` para transformar pixel relativo).

---

## 4. Funcionalidades Centrais

### 4.1 Cubo Isométrico (Isomer.js + Off-Screen)

Isomer aplica transformações no contexto; para não distorcer a grade 2D, usar canvas off-screen:

1. Criar `offscreenCanvas`.
2. `const iso = new Isomer(offscreenCanvas);`
3. `iso.add(Shape.Prism(Point.ORIGIN, w, d, h), color);`
4. No render principal: `ctx.drawImage(offscreenCanvas, targetX, targetY);`

#### API Essencial (Resumo)

| Elemento                 | Uso                                    |
|--------------------------|-----------------------------------------|
| `new Isomer(canvas)`     | Instancia cena isométrica              |
| `Isomer.Point(x,y,z)`    | Ponto base                             |
| `Shape.Prism(p,w,d,h)`   | Prisma / cubo                          |
| `iso.add(shape, color)`  | Adiciona à cena                        |
| `new Color(r,g,b)`       | Cor RGB                                |

### 4.2 Seletor de Direções

Menu → usuário escolhe direção → registra `{ startHex, direction }` → pipeline de linha.

### 4.3 Prolongar Barra até a Borda

Fases:

1. Vetores de direção (cube): `[(1,0,-1), (1,-1,0), (0,-1,1), (-1,0,1), (-1,1,0), (0,1,-1)]`.
2. Raycast lógico: avançar passo a passo até sair dos limites → último válido = `endHex`.
3. `hex_linedraw(startHex, endHex)` (interpolação + round) → caminho.
4. Render: destacar cada hex no caminho.

---

## 5. Arquitetura da Aplicação

### 5.1 Módulos

- `GridLogic.js` – operações puras (conversões, linha, borda).  
- `Renderer.js` – loop, desenho grade, cubo, linhas, pixel→hex usando lógica.
- `StateManager.js` – estado global + pub/sub.
- `UIController.js` – listeners (mouse, menu), traduz eventos em ações de estado.
- `main.js` – orquestra inicialização e wiring.

### 5.2 Fluxo de Interação (Exemplo Linha)

1. Usuário abre menu em tile → estado `activeHex` + mostra menu.
2. Seleciona direção → estado `pendingLine`.
3. Renderer detecta `pendingLine`, consulta `GridLogic.findBorderHex` + `getHexPath`.
4. Armazena caminho e redesenha com destaque.

### 5.3 Boas Práticas & Próximos Passos

- Persistência: serializar tiles + conexões em JSON facilmente.
- Performance: culling / virtualização para grades grandes.
- Testes: `GridLogic` testável isoladamente (Jest/Mocha).  
- Extensões futuras: tipos de conexão, terrenos, custos de pathfinding.

---

## Referências

1. R_241118 JS – (inacessível originalmente)  
2. R_241118 HTML – (inacessível originalmente)  
3. Red Blob Games – Hexagonal Grids  
4. Red Blob Games – Versão v1  
5. eperezcosano – How to draw a hex grid  
6. inspirnathan – Interactive Hexagon Grid (Parte 1)  
7. greentec – Create a hexagonal map  
8. Red Blob – Implementation of Hex Grids  
9. Red Blob – Grid parts and relationships  
10. Honeycomb (site)  
11. honeycomb-grid (npm)  
12. JointJS – Hexagonal Grid demo  
13. Hexmap Library (Open Innovations)  
14. inspirnathan – Hover effects  
15. MDN – getContext  
16. MDN – Pixel manipulation  
17. Medium – honeycomb hex grids  
18. MDN – Drawing shapes  
19. StackOverflow – click in hexagon  
20. JointJS blog – hex grid  
21. Red Blob – more pixel to hex  
22. YouTube – mouse clicks → hex (Unity)  
23. StackOverflow – hexagon click test  
24. Xojo forum – hexagonal button  
25. GameDev.SE – hexagonal clickbox  
26. Konva – context menu  
27. StackOverflow – custom right-click menu  
28. canvas-datagrid – complex context menu  
29. StackOverflow – isometric perspective  
30. GameDev.SE – basic isometric projection  
31. StackOverflow – draw cube  
32. Isomer.js  
33. Isometric cubes article  
34. hex-grid.js repo  
35. Clark Verbrugge – Hex LOS  
36. GameDev.SE – isometric map  
37. Aschenblog – isometric tiling
