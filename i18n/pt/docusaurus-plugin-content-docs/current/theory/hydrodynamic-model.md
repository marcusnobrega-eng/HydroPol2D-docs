---
title: Modelo Hidrodinâmico
---

# Modelo Hidrodinâmico

HydroPol2D inclui atualmente cinco famílias principais de roteamento de superfície:
- inercial local,
- impulso total,
- difusivo D4,
- cinemático D4,
- autômatos celulares.

Apenas uma destas principais formulações de roteamento deve estar ativa por vez. O código atual impõe essa exclusividade da família de roteamento por meio dos sinalizadores de modelo correspondentes. O suporte D8 continua a ser uma via secundária de âmbito limitado.
## 1. Roteamento de fluxo inercial local

### 1.1 Justificativa geral

HydroPol2D usa a **aproximação inercial local** como sua formulação de roteamento hidrodinâmico padrão. O objetivo é manter os controles físicos dominantes do fluxo em águas rasas, evitando ao mesmo tempo a carga computacional das equações completas em águas rasas.
A abordagem inercial local é particularmente atraente para a modelagem de inundações porque preserva:
- o gradiente de pressão da superfície livre,
- aceleração gravitacional,
- resistência ao atrito,
- e aceleração temporal local,

ao mesmo tempo que negligencia os termos de aceleração convectiva que são frequentemente muito menores do que os termos de pressão e atrito em fluxos rasos que variam gradualmente. Isso produz uma formulação que é fisicamente mais consistente do que o roteamento cinemático ou puramente empírico, mas ainda assim muito mais leve do que um solucionador de ondas dinâmicas completo. HydroPol2D usa esta formulação como o principal motor para inundações terrestres, troca de planícies aluviais e redistribuição de águas superficiais através de células raster.
Do ponto de vista da modelagem, a formulação inercial local é um bom compromisso porque HydroPol2D se destina a suportar:
- simulações de inundações causadas por chuvas,
- roteamento fluvial com afluência e limites de estágio,
- aplicações urbanas e de várzea,
- e benchmarks de roteamento controlados em diversas aproximações numéricas,

tudo dentro de uma estrutura hidrológico-hidrodinâmica modular. O modelo inercial local é, portanto, o núcleo hidrodinâmico que conecta os módulos de geração de chuva-escoamento à redistribuição espacial das águas superficiais.
---

### 1.2 Equações governantes

O ponto de partida é a equação de conservação de massa integrada em profundidade:
$$
\frac{\partial h}{\partial t}+
\frac{\partial q_x}{\partial x}+
\frac{\partial q_y}{\partial y}
=
R-
i-
et+
s
$$
onde:
- $h$ é a profundidade da água superficial $[\mathrm{L}]$
- $q_x$ é a descarga unitária na direção $x$ $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $q_y$ é descarga unitária na direção $y$ $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $r$ é a entrada de precipitação $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $i$ é perda de infiltração $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $et$ é a perda de evapotranspiração $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $s$ é a coleção de termos adicionais de origem e destino $[\mathrm{L}\,\mathrm{T}^{-1}]$

No HydroPol2D, os termos hidrológicos são calculados antes do roteamento, e o solucionador inercial local é então usado para avaliar o termo de redistribuição do fluxo.
Para cada face, a equação do momento inercial local é escrita de forma simplificada como
$$
\frac{\partial q}{\partial t}
=-
g\,H_{\mathrm{f}}\,S-
g\,n^2\,\frac{q\,|q|}{H_{\mathrm{f}}^{7/3}}
$$

onde:
- $q$ é a descarga unitária em uma face $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $g$ é aceleração gravitacional $[\mathrm{L}\,\mathrm{T}^{-2}]$
- $H_{\mathrm{f}}$ é a profundidade efetiva do fluxo na face $[\mathrm{L}]$
- $S$ é a inclinação da superfície livre na face $[-]$
- $n$ é o coeficiente de rugosidade de Manning $[\mathrm{T}\,\mathrm{L}^{-1/3}]$

Esta formulação negligencia a aceleração convectiva, mas mantém o equilíbrio hidráulico dominante entre aceleração local, gradiente de pressão e resistência ao atrito do leito.
---

### 1.3 Elevação da superfície da água e declives da face

O cálculo do roteamento começa a partir da elevação da superfície da água em cada célula
$$
\eta = z + h
$$
onde:
- $\eta$ é a elevação da superfície da água $[\mathrm{L}]$
- $z$ é a elevação da cama $[\mathrm{L}]$
- $h$ é a profundidade da água $[\mathrm{L}]$

Na implementação validada padrão, HydroPol2D usa a elevação do leito DEM diretamente para cálculos de inclinação.
Na face leste entre as células $i$ e $i+1$, a elevação do leito da face é considerada como
$$
z_{\mathrm{f},x} = \max\!\left(z_i,\;z_{i+1}\right)
$$
e as elevações da superfície da água reconstruídas hidrostaticamente são
$$
\eta_{\mathrm{L},x}^{\ast} = \max\!\left(\eta_i,\;z_{\mathrm{f},x}\right)
\qquad
\eta_{\mathrm{R},x}^{\ast} = \max\!\left(\eta_{i+1},\;z_{\mathrm{f},x}\right)
$$
A inclinação da superfície livre na face é então calculada como
$$
S_x = \frac{\eta_{\mathrm{R},x}^{\ast} - \eta_{\mathrm{L},x}^{\ast}}{\Delta x}
$$
Da mesma forma, para uma face norte-sul,
$$
z_{\mathrm{f},y} = \max\!\left(z_j,\;z_{j+1}\right)
$$
$$
\eta_{\mathrm{S},y}^{\ast} = \max\!\left(\eta_j,\;z_{\mathrm{f},y}\right)
\qquad
\eta_{\mathrm{N},y}^{\ast} = \max\!\left(\eta_{j+1},\;z_{\mathrm{f},y}\right)
$$
$$
S_y = \frac{\eta_{\mathrm{S},y}^{\ast} - \eta_{\mathrm{N},y}^{\ast}}{\Delta x}
$$
Esta reconstrução hidrostática é essencial perto de frentes úmidas-secas porque evita profundidades negativas não físicas e garante que o gradiente de pressão seja avaliado apenas sobre a porção molhada hidraulicamente conectada da interface. Em termos práticos, é um dos principais ingredientes estabilizadores da implementação inercial local do HydroPol2D.
---

### 1.4 Profundidade facial efetiva

A profundidade hidráulica efetiva usada na equação do momento é calculada no nível da face.
Para o caso de grade grossa padrão, a profundidade da face é
$$
H_{\mathrm{f},x}
=
\max\!\left(
\max(\eta_i,\eta_{i+1}) - z_{\mathrm{f},x},
0
\right)
$$
e da mesma forma na direção $y$.
Assim, a profundidade da face não é simplesmente a média aritmética das profundidades das células vizinhas. Em vez disso, é uma profundidade reconstruída hidrostaticamente, referenciada à elevação mais alta do leito na interface. Isto torna o modelo muito mais robusto quando células adjacentes têm diferentes elevações de leito ou quando um lado está quase seco. A mesma definição conceitual já está declarada em seu documento de referência.
---

### 1.5 Solucionador inercial local discreto

HydroPol2D atualiza a descarga facial explicitamente a tempo. A forma discreta de base usada no esquema original do tipo Bates é
$$
q^{t+\Delta t}
=
\frac{
q^{t}-
g\,H_{\mathrm{f}}\,\Delta t\,S
}{
1+
g\,\Delta t\,n^2
\,\dfrac{|q^{t}|}{H_{\mathrm{f}}^{7/3}}
}
$$

onde:
- $q^{t}$ é a descarga facial anterior $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $q^{t+\Delta t}$ é a descarga facial atualizada $[\mathrm{L}^2\,\mathrm{T}^{-1}]$
- $\Delta t$ é o intervalo de tempo $[\mathrm{T}]$

Esta é a forma exata implementada em `Inertial_Solver` quando `flag_numerical_scheme = 1`.
A estrutura desta equação é importante:
- o numerador contém a memória inercial da etapa anterior e o termo de condução de superfície livre,
- o denominador contém o amortecimento friccional,
- então o esquema se comporta como um preditor explícito com tratamento de atrito semi-implícito.

É por isso que o método é estável e eficiente para simulações de inundações rasas.
---

### 1.6 Esquemas numéricos disponíveis em HydroPol2D

HydroPol2D suporta três variantes inerciais locais:
- esquema Bates original,
- Esquema $s$-upwind,
- Esquema centrado em $s$.

Estes são controlados por `flag_numerical_scheme`.
#### 1.6.1 Esquema 1: formulação original de Bates

Esta é a atualização inercial local discreta mais simples e direta:
$$
q^{t+\Delta t}
=
\frac{
q^{t}-
g\,H_{\mathrm{f}}\,\Delta t\,S
}{
1+
g\,\Delta t\,n^2
\,\dfrac{|q^{t}|}{H_{\mathrm{f}}^{7/3}}
}
$$

É computacionalmente eficiente e fisicamente consistente, mas em configurações de gradiente acentuado ou fortemente descontínuas pode ser mais propenso a comportamento oscilatório do que os esquemas modificados.
#### 1.6.2 Esquema 2: formulação $s$-upwind

A versão upwind introduz uma estimativa de descarga direcional $q_{\mathrm{upwind}}$ e a combina com a descarga frontal atual usando um fator de difusividade $\theta$:
$$
q^{t+\Delta t}
=
\frac{
\thetaq^{t}+
(1-\theta) q_{\mathrm{upwind}}-
g\,H_{\mathrm{f}}\,\Delta t\,S
}{
1+
g\,\Delta t\,n^2
\,\dfrac{|q^{t}|}{H_{\mathrm{f}}^{7/3}}
}
$$

O fator de difusividade é calculado como
$$
\teta
=
1-
\frac{\Delta t}{\Delta x}
\min\!\left(\frac{|q|}{H_{\mathrm{f}}},
\sqrt{g\,H_{\mathrm{f}}}
\right)
$$
Esta quantidade introduz difusão numérica controlada. Em termos práticos:
- quando o fluxo é lento e bem resolvido, $\theta$ permanece próximo de $1$ e o esquema se comporta como a atualização inercial local original;
- quando o fluxo se torna rápido ou o intervalo de tempo se aproxima do limite local de Courant, o esquema muda parte da atualização em direção ao fluxo contra o vento, o que amortece as oscilações.

É por isso que a variante contra o vento é útil em condições de rota mais desafiadoras.
#### 1.6.3 Esquema 3: Formulação centrada em $s$

O esquema centrado substitui a descarga contra o vento por uma média vizinha centrada:
$$
q_{\mathrm{avg}}
=
\frac{q_{i-1} + q_{i+1}}{2}
$$
e atualiza a quitação conforme
$$
q^{t+\Delta t}
=
\frac{
\thetaq^{t}+
(1-\theta) q_{\mathrm{avg}}-
g\,H_{\mathrm{f}}\,\Delta t\,S
}{
1+
g\,\Delta t\,n^2
\,\dfrac{|q^{t}|}{H_{\mathrm{f}}^{7/3}}
}
$$

Este esquema é mais simétrico que a versão upwind e menos difusivo, mas ainda usa o mesmo coeficiente $\theta$ para suprimir a instabilidade. Na prática, proporciona um compromisso entre a resposta mais nítida da forma Bates original e o amortecimento mais forte da forma contra o vento.
---

### 1.7 Tratamento úmido-seco e profundidade operatória mínima

HydroPol2D contém diversas proteções explícitas para evitar roteamento não físico em interfaces secas ou inválidas.
Um rosto é suprimido se:
- a profundidade efetiva da face é zero,
- uma das células vizinhas está fora do domínio válido,
- ou a profundidade da célula local está abaixo de um limite operacional mínimo.

Em termos de código, HydroPol2D zera:
- inclinação do rosto,
- profundidade eficaz,
- e largura efetiva da face

sempre que um rosto está seco ou inválido. Em seguida, aplica uma lógica adicional para águas rasas com base em uma profundidade operacional mínima $h_{\min}$. Se a profundidade atual da célula estiver abaixo de $h_{\min}$, os fluxos de faces vizinhas serão zerados para suprimir movimentos espúrios em células quase secas. No caso padrão, o código usa $h_{\min}=10^{-6}\,\mathrm{m}$, embora possa ser definido como zero quando hidrogramas de afluência estão sendo impostos.
Esta lógica húmida-seca é uma das razões pelas quais o modelo permanece robusto nas fases de expansão e recessão das cheias.
---

### 1.9 Conversão de unidades e escrituração de quitação facial

Internamente, o solucionador inercial funciona com **descarga unitária** $q$ em
$$
[\mathrm{L}^2\,\mathrm{T}^{-1}]
\quad\text{that is,}\quad
[\mathrm{m}^2\,\mathrm{s}^{-1}]
$$
O código primeiro converte o estado atual do fluxo de saída de unidades de profundidade baseadas em células em descarga de unidade baseada em face. Após a atualização inercial local ser realizada, o modelo converte novamente para descarga volumétrica por face:
$$
Q = q\,W_{\mathrm{f}}
$$
e então para uma taxa de profundidade equivalente sobre a área da célula:
$$
q_{\mathrm{mm/h}}
=
\frac{Q}{A_{\mathrm{cell}}}
\,
1000
\,
3600
$$
onde:
- $A_{\mathrm{cell}}$ é a área da célula $[\mathrm{L}^2]$

Esta contabilidade é necessária porque HydroPol2D acopla os fluxos hidrodinâmicos a termos hidrológicos que são rastreados em unidades de profundidade como $\mathrm{mm}$ ou $\mathrm{mm/h}$.
---

### 1.10 Limites de fluxo físico

HydroPol2D impõe duas restrições físicas adicionais após a atualização inercial.
#### 1.10.1 Limite de fluxo crítico

Se o limitador de fluxo crítico estiver ativo, a magnitude da descarga da unidade é limitada por
$$
|q| \le H_{\mathrm{f}} \sqrt{g\,H_{\mathrm{f}}}
$$

Isto evita que o solucionador inercial produza velocidades que excedam a condição crítica local.
#### 1.10.2 Limite máximo de velocidade

HydroPol2D também impõe um limite rígido de velocidade máxima, atualmente definido como
$$
u_{\max} = 10 \;\mathrm{m\,s}^{-1}
$$
O limite de descarga unitária correspondente é
$$
|q| \le H_{\mathrm{f}}\,u_{\max}
$$

Esta é uma salvaguarda numérica pragmática contra picos isolados causados ​​por profundidade abrupta ou descontinuidades de taludes.
---

### 1.11 Atualização de continuidade e equilíbrio de volume de células

Uma vez calculadas as descargas faciais, HydroPol2D atualiza cada célula integrando a divergência líquida do fluxo ao longo do intervalo de tempo.
No nível da célula, o equilíbrio do volume intercelular pode ser escrito conceitualmente como
$$
\Delta V
=
\Delta t
\left(
Q_{\mathrm{in}} - Q_{\mathrm{out}}
\right)
$$
A profundidade da água atualizada é então
$$
h^{t+\Delta t}
=
h^t+
\frac{\Delta V}{A_{\mathrm{eff}}}
$$
onde:
- $A_{\mathrm{eff}}$ é a área de armazenamento efetiva da célula $[\mathrm{L}^2]$

No fluxo de trabalho de grade grossa validado, $A_{\mathrm{eff}}$ é a área da célula.
O código então impõe
$$
h^{t+\Delta t} \ge 0
$$
para que profundidades de água negativas nunca sejam permitidas.
---

### 1.12 Condições limite de saída

HydroPol2D suporta dois tratamentos de saída no solucionador inercial local.
#### 1.12.1 Saída de profundidade normal

Quando `outlet_type = 1`, a inclinação de saída é imposta como uma inclinação de fluxo normal prescrita
$$
S_0 = s_{\mathrm{outlet}}
$$
e a descarga de saída é calculada com a equação de Manning.
#### 1.12.2 Saída de profundidade crítica

Quando `outlet_type \ne 1`, HydroPol2D calcula um controle de saída tipo inclinação crítica a partir da profundidade e rugosidade local. Em ambos os casos, o fluxo de saída é convertido para uma taxa equivalente à profundidade e subtraído da profundidade final da água durante a atualização.
Este tratamento de saída permite que o solucionador inercial local permaneça incorporado dentro de um domínio raster enquanto ainda aplica uma condição de contorno fisicamente interpretável no perímetro do domínio.
---

### 1.13 Interação reservatório e controle hidráulico

O solucionador inercial local também pode ser modificado internamente por armazenamento ou controles de curva nominal. Quando o roteamento do reservatório está ativo, HydroPol2D impõe relações de descarga na forma
$$
Q = k\,(h-h_0)^m
$$
sujeito a restrições de água disponível e conexões a jusante definidas pelo usuário. Na implementação atual, a lógica de controle de dois estágios é suportada. O volume descarregado resultante é transferido diretamente para células designadas a jusante.
Isto significa que o solucionador inercial local não é um bloco de roteamento fechado; é um núcleo de roteamento que pode ser modificado localmente por estruturas de controle hidráulico.
---

### 1.14 Por que o modelo inercial local é o padrão em HydroPol2D

A formulação inercial local é o método de roteamento padrão em HydroPol2D por três motivos.
Primeiro, mantém a hidráulica dominante necessária para a propagação das inundações:
- gradiente de pressão de superfície livre,
- atrito,
- aceleração local.

Em segundo lugar, é computacionalmente eficiente o suficiente para ser usado em grandes domínios raster e em execução de GPU.
Terceiro, integra-se naturalmente com o acoplamento de processo validado do HydroPol2D:
- controles hidráulicos,
- condições de saída,
- e acoplamento hidrológico fonte-sumidouro.

Por estas razões, fornece o melhor equilíbrio entre realismo físico e tratabilidade computacional para a maioria das aplicações HydroPol2D.
---

### 1.15 Modelo subgrade de Neal (2012)

O HydroPol2D inclui a formulação retangular de canal subgrade proposta por [Neal et al. (2012)](https://doi.org/10.1029/2012WR012514). Essa extensão é usada quando o rio é mais estreito que a célula raster. O canal é embutido na célula grosseira, enquanto o escoamento bidimensional continua sendo calculado na planície ao redor do canal.

Seja $\Delta x$ a largura da célula, $z_f$ a elevação da planície, $H$ a altura da margem e $w$ a largura do canal, com $0<w<\Delta x$. A elevação do leito do canal é

$$
z_c=z_f-H.
$$

A profundidade $h$ é medida acima de $z_c$. A água permanece no canal retangular quando $h\le H$ e se espalha pela célula grosseira quando $h>H$.

#### Escoamento no canal em uma face

A elevação da superfície da água no canal é

$$
y_c=z_c+h.
$$

Para células adjacentes $i$ e $j$, a declividade da superfície e a profundidade de escoamento na face são

$$
S_c=\frac{y_{c,j}-y_{c,i}}{\Delta x},
$$

$$
h_{c,f}=\max\!\left[\max(y_{c,i},y_{c,j})-
\max(z_{c,i},z_{c,j}),0\right].
$$

A largura compartilhada do canal é

$$
w_{c,f}=\min(w_i,w_j).
$$

A área de escoamento e o raio hidráulico do canal são

$$
A_c=w_{c,f}h_{c,f},
\qquad
R_c=\frac{A_c}{w_{c,f}+2h_{c,f}}.
$$

A vazão no canal é atualizada pela equação inercial local

$$
Q_c^{t+\Delta t}=
\frac{Q_c^t-gA_c\Delta t S_c}
{1+g\Delta t n_c^2|Q_c^t|/(R_c^{4/3}A_c)},
$$

em que $n_c$ é o coeficiente de Manning do canal.

#### Escoamento na planície em uma face

A profundidade na planície é medida acima do DEM grosseiro:

$$
h_f=\max(h+z_c-z_f,0),
\qquad y_f=z_f+h_f.
$$

A declividade e a profundidade na face da planície são calculadas a partir de $y_f$ e $z_f$, da mesma forma que os termos do canal. A atualização inercial local usa a vazão unitária $q_f$:

$$
q_f^{t+\Delta t}=
\frac{q_f^t-gh_{f,f}\Delta t S_f}
{1+g\Delta t n_f^2|q_f^t|/h_{f,f}^{7/3}},
$$

em que $n_f$ é o coeficiente de Manning da planície. As vazões da planície e da face completa são

$$
Q_f=q_f(\Delta x-w_{c,f}),
\qquad
Q=Q_c+Q_f.
$$

O HydroPol2D aplica essa separação nas faces ortogonais D4. A saída usa os mesmos componentes de canal e planície empregados nas faces internas.

#### Transição conservativa do armazenamento

A equação de continuidade da célula é avaliada em termos de volume. Para uma célula com canal,

$$
V(h)=
\begin{cases}
\Delta x\,w\,h, & h\le H,\\[4pt]
\Delta x\,w\,H+\Delta x^2(h-H), & h>H.
\end{cases}
$$

Assim, a área ativa da superfície $\mathrm{d}V/\mathrm{d}h$ muda de $\Delta xw$, dentro das margens, para $\Delta x^2$, acima das margens. Os fluxos de roteamento e os termos hidrológicos de fonte ou sumidouro atualizam primeiro $V$. Em seguida, o HydroPol2D inverte a mesma relação por partes para recuperar $h$. Esse procedimento evita uma descontinuidade de massa na passagem pela altura da margem.

A configuração ativa e os dados geométricos são descritos em [Bandeiras do modelo](../configuration/flags). Os resultados dos testes controlados são apresentados em [Validação do modelo subgrade de Neal (2012)](../validation/neal-subgrid).

### 1.16 Resumo

Em HydroPol2D, o Modelo Inercial Local é uma formulação de roteamento baseada em raster com integração profunda na qual:
- a elevação da superfície da água celular é primeiro reconstruída,
- inclinações de superfície livre são avaliadas nas faces,
- as profundidades efetivas da face são calculadas hidrostaticamente,
- descargas faciais são atualizadas com uma equação inercial local do tipo Bates,
- os fluxos resultantes são convertidos em descargas volumétricas,
- e a profundidade da água é atualizada por um equilíbrio conservador do volume celular.

O solucionador suporta:
- o esquema Bates original,
- um esquema estabilizado contra o vento,
- um esquema estabilizado centrado,
- controles de saída,
- controles de reservatório,
- manuseio frontal molhado-seco,
- limites de fluxo crítico e velocidade.

Isso o torna o principal motor hidrodinâmico do HydroPol2D para roteamento de fluxo de superfície com base física.
---

## 2. Roteamento de fluxo de impulso total

### 2.1 Justificativa geral

HydroPol2D também inclui um **solucionador de momento total para águas rasas** para casos em que a aproximação inercial local não é suficiente. Esta opção destina-se a benchmarks hidráulicos controlados e aplicações onde a aceleração convectiva, a propagação de ondas ou efeitos dinâmicos mais fortes precisam ser representados de forma mais explícita.
O modelo de momento total resolve as equações bidimensionais conservadoras de águas rasas na grade raster. No HydroPol2D, isso é implementado como um núcleo de roteamento de volume finito com armazenamento explícito e estados de momento.
O solucionador é ativado por meio do sinalizador de roteamento full-momentum na configuração do modelo. Deve ser usado como uma alternativa, não simultaneamente, ao roteamento local inercial, cinemático, difusivo, D8 ou CA.
---

### 2.2 Equações conservadoras para águas rasas

O vetor de estado conservado é
$$
\mathbf{U}
=
\begin{bmatrix}
h\\
eh \\
hv
\end{bmatrix}
$$
onde:
- $h$ é a profundidade da água $[\mathrm{L}]$
- $u$ é a velocidade média de profundidade na direção $x$ $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $v$ é a velocidade média da profundidade na direção $y$ $[\mathrm{L}\,\mathrm{T}^{-1}]$
- $hu$ e $hv$ são descargas unitárias ou variáveis ​​​​de momento $[\mathrm{L}^2\,\mathrm{T}^{-1}]$

As equações governantes são escritas como
$$
\frac{\partial \mathbf{U}}{\partial t}+
\frac{\partial \mathbf{F}(\mathbf{U})}{\partial x}+
\frac{\partial \mathbf{G}(\mathbf{U})}{\partial y}
=
\mathbf{S}_{\mathrm{bed}}+
\mathbf{S}_{\mathrm{fric}}
$$
com fluxos
$$
\mathbf{F}(\mathbf{U})
=
\begin{bmatrix}
eh \\
\dfrac{(hu)^2}{h} + \dfrac{1}{2}gh^2 \\
\dfrac{(hu)(hv)}{h}
\end{bmatrix}
$$
e
$$
\mathbf{G}(\mathbf{U})
=
\begin{bmatrix}
hv \\
\dfrac{(hu)(hv)}{h} \\
\dfrac{(hv)^2}{h} + \dfrac{1}{2}gh^2
\end{bmatrix}
$$
onde $g$ é a aceleração gravitacional.
Os termos de origem da inclinação do leito representam o forçamento topográfico:
$$
\mathbf{S}_{\mathrm{bed}}
=
\begin{bmatrix}
0 \\
-gh\,\dfrac{\partial z}{\partial x} \\
-gh\,\dfrac{\partial z}{\partial y}
\end{bmatrix}
$$
e os termos da fonte de atrito representam a resistência Manning.
---

### 2.3 Fluxos numéricos e memória de momento

HydroPol2D calcula fluxos de momento total com um solucionador de volume finito do tipo HLL. Em cada face da célula, os estados reconstruídos à esquerda e à direita são usados ​​para calcular o fluxo de massa e o fluxo de momento. A atualização é conservadora no sentido de que o fluxo que sai de uma célula entra na célula adjacente com sinal oposto.
Ao contrário do solucionador inercial local, o modelo de momento total deve transportar o momento de um passo de tempo para o seguinte. Lojas HydroPol2D:
- o atual estado $hu$ centrado na célula,
- o estado atual $hv$ centrado na célula,
- fluxos de massa facial convertidos de volta para unidades de taxa de profundidade HydroPol2D,
- termos do coletor de saída.

Essa memória de momento é o que torna o modelo um verdadeiro solucionador de ondas dinâmicas, em vez de um recálculo de descarga baseado apenas na inclinação atual da superfície da água.
---

### 2.4 Inclinação do leito, fricção e tratamento de umedecimento e secagem

O solucionador de momento total inclui diversas proteções numéricas para simulação de inundação raster:
- as células secas e inativas são tratadas como paredes sólidas;
- células muito rasas são limpas para evitar velocidades indefinidas;
- o momento é limitado por uma velocidade máxima admissível;
- O atrito Manning é aplicado com uma atualização implícita semi-implícita ou exata;
- um limitador de drenagem evita que o fluxo facial remova mais água do que a disponível.

A atualização de fricção Manning amortece o impulso de acordo com a profundidade local, rugosidade e magnitude da velocidade. Conceitualmente, os componentes do momento são relaxados por um denominador da forma
$$
1 + g\,n^2\,\Delta t\,\frac{\sqrt{u^2+v^2}}{h^{4/3}}
$$
onde $n$ é o coeficiente de rugosidade de Manning. Isso evita um grande impulso irrealista em águas rasas, ao mesmo tempo que mantém a propagação dinâmica onde a profundidade da água é suficiente.
A reconstrução hidrostática está disponível para terrenos complexos e tratamento de talude de leito bem balanceado, enquanto o caminho de referência controlado padrão usa o robusto tratamento de fluxo/fonte HLL implementado no solucionador atual.
---

### 2.5 Atualização de continuidade e acoplamento HydroPol2D

Depois que os fluxos HLL são calculados, a atualização da profundidade segue o equilíbrio de volume finito:
$$
h^{t+\Delta t}
=
h^t-
\frac{\Delta t}{\Delta x}
\left(
F_h^{E} - F_h^{W}+
G_h^{N} - G_h^{S}
\right)
$$
onde $F_h$ e $G_h$ são os componentes do fluxo de massa através das faces da célula.
HydroPol2D então converte os fluxos de face para a mesma convenção de contabilidade usada pelo resto do modelo:
$$
q_{\mathrm{mm/h}}
=
\frac{Q}{A_{\mathrm{cell}}}
1000
3600
$$
Isso permite que o solucionador de momento total permaneça compatível com termos de fonte/sumidouro hidrológico, transporte de qualidade da água, controles de reservatório e diagnóstico de condições de contorno.
---

### 2.6 Condições limite e controles hidráulicos

O modelo full-momentum suporta a mesma arquitetura prática de condições de contorno usada pelo roteamento HydroPol2D:
- paredes reflexivas fechadas ao longo de faces inativas ou externas,
- células coletoras de saída com comportamento de profundidade normal ou profundidade crítica,
- limites impostos do hidrograma de afluência,
- limites prescritos do hidrograma de estágio,
- reservatório e estruturas internas de controle da curva nominal.

Para fronteiras fechadas, o fluxo de massa normal é zero, mas os efeitos da pressão de parede são contabilizados na atualização do momento. Isto é importante para um comportamento estável próximo às bordas do domínio e células inativas.
Os fluxos de saída são convertidos em um sumidouro de volume e removidos do armazenamento de água local, sujeitos às restrições de água disponível.
---

### 2.7 Evidências de validação atuais

O solucionador de impulso total faz parte do pacote de validação da validação. As evidências atuais prontas para relatório incluem:
- escoamento em plano inclinado contra o limite analítico da onda cinemática;
- Conservação de massa de captação inclinada em V e verificações de simetria bilateral;
- Perfis analíticos de ruptura de barragens em leito seco de Ritter;
- propagação de ondas ininterruptas e comparação de perfis;
- aplicação prescrita do limite do estágio;
- hidrograma de afluência e contabilidade de reservatório/estrutura de controle onde a rota de momento total é usada.

Esses testes validam a implementação de impulso total como uma opção de roteamento de ondas dinâmicas controladas. Eles não implicam calibração de campo para uma determinada bacia hidrográfica.
---

### 2.8 Uso prático do solver full momentum

O solver full momentum é indicado para simulações em que os termos adicionais de advecção e aceleração local justificam o custo computacional maior. No HydroPol2D, ele deve ser tratado como uma escolha própria de família de roteamento, e não como um complemento aos modos mais leves.
---

## 3. Roteamento D4 difusivo e cinemático

HydroPol2D implementa roteamento de onda **difusivo** e **cinemático** por meio de um solucionador D4 conservador compartilhado. Esses modos são mais leves que os solucionadores inerciais locais e de momento total, mas ainda usam fluxos explícitos baseados em faces, atualizações conservadoras de volume, manipulação de saída e acoplamento reservatório/controle.
### 3.1 Estrutura de roteamento conservadora compartilhada

Em ambos os modos, HydroPol2D direciona a água através dos quatro vizinhos ortogonais de cada célula e atualiza a profundidade da célula através de um equilíbrio de volume conservador:
$$
h^{t+\Delta t}
=
h^t+
\frac{V_{\mathrm{in}} - V_{\mathrm{out}}}{A_{\mathrm{cell}}}
$$
onde:
- $h$ é a profundidade da água na célula $[\mathrm{L}]$
- $V_{\mathrm{in}}$ e $V_{\mathrm{out}}$ são volumes de entrada e saída na subetapa $[\mathrm{L}^3]$
- $A_{\mathrm{cell}}$ é a área da célula ativa $[\mathrm{L}^2]$

O intervalo de roteamento é subdividido internamente quando necessário. O código atual estima o número de subetapas de uma estimativa de velocidade do tipo Manning e uma meta do estilo Courant para que encostas íngremes ou águas profundas não desestabilizem a atualização explícita.
### 3.2 Modo difusivo

No modo difusivo, a inclinação de condução é a **inclinação da superfície da água** entre células adjacentes. Para um rosto compartilhado pelas células esquerda e direita,
$$
\eta = z + h
$$
$$
S_f = \frac{\eta_L - \eta_R}{\Delta x}
$$
com profundidade de face reconstruída hidrostaticamente
$$
H_f = \max\!\left(\max(\eta_L,\eta_R) - z_f,\,0\right)
$$
A descarga da unidade frontal é então avaliada com uma lei de fluxo do tipo Manning:
$$
q_f
=
\nomedooperador{sign}(S_f)
\frac{H_f^{5/3}}{n}\sqrt{|S_f|}
$$

Este modo pode representar uma redistribuição tipo remanso impulsionada por gradientes da superfície da água, embora permaneça muito mais barato do que resolver uma equação de momento.
### 3.3 Modo cinemático

No modo cinemático, a inclinação de condução é a **inclinação do leito**, e não a inclinação da superfície da água:
$$
S_b = \frac{z_L - z_R}{\Delta x}
$$
O código então aplica uma regra de profundidade do doador:
- se $S_b > 0$, a célula esquerda é a doadora e sua profundidade impulsiona o fluxo,
- se $S_b &lt; 0$, a célula direita é a doadora e sua profundidade impulsiona o fluxo.

Usando a profundidade do doador $H_{\mathrm{donor}}$, a descarga da unidade é
$$
q_f
=
\nomedooperador{sign}(S_b)
\frac{H_{\mathrm{donor}}^{5/3}}{n_{\mathrm{donor}}}\sqrt{|S_b|}
$$

Isso torna a rota cinemática estritamente direcionada à inclinação e evita que ela represente o mesmo comportamento de remanso capturado pelos solucionadores difusivos, inerciais ou de momento total.
### 3.4 Controles compartilhados, manuseio de saída e acoplamento

Ambos os modos de onda D4 compartilham o mesmo mecanismo de roteamento conservador para:
- subpasso interno,
- limitação de armazenamento disponível para que uma célula doadora não possa exportar mais volume do que contém,
- limitação opcional de fluxo crítico,
- remoção de descarga de saída,
- interação entre reservatório e controle hidráulico.

Tal como acontece com as outras famílias de roteamento, precipitação, infiltração, evapotranspiração, feedback de águas subterrâneas e outros termos de fonte/sumidouro são tratados pela estrutura acoplada HydroPol2D em torno da atualização de roteamento.
### 3.5 Escopo e advertências

Os modos difusivo e cinemático D4 fazem parte da família de roteamento implementada e são usados ​​nos atuais benchmarks de validação controlada. No entanto:
- eles devem ser tratados como alternativas, e não como combinações, com inercial local ou momento total,
- O apoio D8 deve ser considerado um caminho secundário de escopo limitado, em vez de uma família de teorias paralelas,
---

## 4. Roteamento de fluxo de autômatos celulares

### 4.1 Formulação conceitual

Além do modelo inercial local, HydroPol2D fornece um **esquema de roteamento de autômato celular (CA)** como uma alternativa simplificada para propagação de fluxo de superfície.
O modelo CA é baseado na **redistribuição local do volume de água entre células vizinhas**, impulsionada por diferenças na elevação da superfície da água. Ao contrário da formulação inercial local, esta abordagem:
- não resolve explicitamente uma equação de momento,
- não rastreia velocidade ou descarga nas faces,
- depende de regras empíricas de redistribuição de fluxo,
- garante estrita conservação de massa no nível celular.

Esta formulação é particularmente útil para:
- estimativa rápida da extensão da inundação,
- simulações em grande escala onde a eficiência computacional é crítica,
- casos onde a dinâmica hidráulica detalhada não é necessária.

---

### 4.2 Representação da superfície da água

Tal como no modelo inercial, a variável determinante é a elevação da superfície da água:
$$
\eta = z + h
$$
onde:
- $\eta$ = elevação da superfície da água $[\mathrm{L}]$
- $z$ = elevação do leito $[\mathrm{L}]$
- $h$ = profundidade da água $[\mathrm{L}]$

---

### 4.3 Gradiente de condução e direção do fluxo

O fluxo entre uma célula $i$ e uma célula vizinha $j$ é impulsionado pela diferença:
$$
\Delta \eta_{i,j} = \eta_i - \eta_j
$$
Apenas gradientes positivos contribuem para o fluxo:
$$
\Delta\eta_{i,j} > 0
$$
Isso garante que a água flua apenas **descendo em termos de superfície livre**, evitando o refluxo não físico.
---

### 4.4 Volume transferível disponível

O volume potencial que pode ser transferido da célula $i$ para o vizinho $j$ é estimado como:
$$
V_{i,j} = A_{\mathrm{cell}} \cdot \max(\Delta \eta_{i,j}, 0)
$$
onde:
- $V_{i,j}$ = volume transferível $[\mathrm{L}^3]$
- $A_{\mathrm{cell}}$ = área da célula $[\mathrm{L}^2]$

---

### 4.5 Particionamento de fluxo

O volume total transferível de uma célula é distribuído entre seus vizinhos proporcionalmente:
$$
w_{i,j} =
\frac{
V_{i,j}
}{
\sum_k V_{i,k} + \varepsilon
}
$$
onde:
- $w_{i,j}$ = peso atribuído ao vizinho $j$
- $\varepsilon$ = pequena constante numérica para evitar divisão por zero

A saída total da célula é então:
$$
I_{i,j} = w_{i,j} \cdot I_{\mathrm{tot}}
$$
onde:
- $I_{\mathrm{tot}}$ = volume total de saída $[\mathrm{L}^3]$

---

### 4.6 Estimativa de velocidade

Embora o modelo CA não resolva explicitamente as equações de momento, uma velocidade característica é estimada usando a equação de Manning:
$$
u = \frac{1}{n} h^{2/3} S^{1/2}
$$
onde:
- $u$ = velocidade do fluxo $[\mathrm{L}\mathrm{T}^{-1}]$
- $n$ = coeficiente Manning $[\mathrm{T}\mathrm{L}^{-1/3}]$
- $S$ = inclinação $[-]$

Esta velocidade é usada para controlar a **taxa de redistribuição da água**.
---

### 4.7 Cálculo de saída

A saída total de uma célula é calculada como:
$$
I_{\mathrm{tot}} = u \cdot h \cdot \Delta t \cdot W_{\mathrm{eff}}
$$
onde:
- $I_{\mathrm{tot}}$ = volume total de saída $[\mathrm{L}^3]$
- $\Delta t$ = intervalo de tempo $[\mathrm{T}]$
- $W_{\mathrm{eff}}$ = largura efetiva do fluxo $[\mathrm{L}]$

---

### 4.8 Atualização de profundidade

Após a redistribuição, a profundidade da água é atualizada como:
$$
h^{t+\Delta t}
=
h^t+
\frac{
\soma Q_{\mathrm{in}} - \soma Q_{\mathrm{out}}
}{
A_{\mathrm{cell}}
}
$$
onde:
- $Q_{\mathrm{in}}$ = volume de entrada $[\mathrm{L}^3]$
- $Q_{\mathrm{out}}$ = volume de saída $[\mathrm{L}^3]$

O modelo impõe:
$$
h^{t+\Delta t} \ge 0
$$
garantindo consistência física.
---

### 4.9 Estabilidade e robustez

O modelo CA é inerentemente estável porque:
- o fluxo é limitado pelo volume de água disponível,
- a redistribuição é limitada por gradientes locais,
- nenhum termo de aceleração explícito está presente.

No entanto, o método é:
- mais difusivo que o Modelo Inercial Local,
- menos preciso para representar processos hidráulicos dinâmicos,
- não é adequado para capturar a propagação de ondas ou efeitos de remanso.

---

### 4.10 Comparação com Modelo Inercial Local

| Recurso | Modelo Inercial Local | Autômatos Celulares |
|--------|----------------------|-------------------|
| Física | Baseado em impulso | Empírico |
| Variáveis | $q$, $h$, $\eta$ | $h$, $\eta$ |
| Precisão | Alto | Moderado |
| Estabilidade | Condicional | Muito alto |
| Custo computacional | Moderado | Baixo |
| Dinâmica de inundação | Bem capturado | Difusivo |

---

### 4.11 Quando usar o modelo CA

O modelo Cellular Automata é recomendado quando:
- simulações em grande escala são necessárias,
- a velocidade computacional é uma prioridade,
- apenas a extensão da inundação ou profundidades aproximadas são necessárias,
- o comportamento hidráulico detalhado não é crítico.

Para a propagação de inundações com base física, o **Modelo Inercial Local continua sendo a opção preferida**.
---

## Resumo

HydroPol2D oferece suporte a uma família de roteamento que agora inclui publicamente:
- **roteamento inercial local** como solucionador de inundação com base física padrão,
- **Roteamento de impulso total** para benchmarks de ondas dinâmicas e efeitos de impulso mais fortes,
- **Roteamento difusivo D4** impulsionado pela inclinação da superfície da água,
- **Roteamento cinemático D4** conduzido pela inclinação do leito e profundidade do doador,
- **Roteamento de autômatos celulares** para redistribuição rápida e simplificada.

Todas essas rotas compartilham o acoplamento mais amplo do HydroPol2D com entradas hidrológicas, feedback de águas subterrâneas, contabilidade de saída e controles hidráulicos, mas apenas uma formulação principal de rota deve estar ativa em uma determinada rota. O D8 permanece de escopo secundário.
