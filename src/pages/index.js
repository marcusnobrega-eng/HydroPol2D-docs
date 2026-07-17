import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {
  Droplets,
  Waves,
  Mountain,
  FlaskConical,
  ArrowRight,
  Cpu,
  Map,
  ShieldCheck,
  Gauge,
  CloudRain,
  Trees,
  Snowflake,
  CloudSun,
  Layers3,
  Database,
  MoveDown,
  Factory,
  Orbit,
  Sparkles,
  ArrowDownCircle,
  ArrowUpCircle,
  Workflow,
} from 'lucide-react';

import styles from './index.module.css';

function ProcessCard({ icon, title, subtitle, items, accent }) {
  return (
    <div className={`${styles.processCard} ${styles[accent] || ''}`}>
      <div className={styles.processCardHeader}>
        <div className={styles.processIconWrap}>{icon}</div>
        <div>
          <h3>{title}</h3>
          <p>{subtitle}</p>
        </div>
      </div>

      <div className={styles.processList}>
        {items.map((item, idx) => (
          <div key={idx} className={styles.processItem}>
            <span className={styles.processBullet}></span>
            <span>{item}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function CouplingPill({ icon, text }) {
  return (
    <div className={styles.couplingPill}>
      {icon}
      <span>{text}</span>
    </div>
  );
}

export default function Home() {
  const {i18n, siteConfig} = useDocusaurusContext();
  const currentLocale = i18n.currentLocale;
  const siteBaseUrl = siteConfig.baseUrl;
  const logoUrl = useBaseUrl('/img/logo.svg');
  const docsUrl = useBaseUrl('/docs/getting-started/overview');
  const validationUrl = useBaseUrl('/docs/validation/overview');
  const languageOptions = [
    {code: 'en', label: 'English', flag: '🇺🇸', to: `${siteBaseUrl}docs/getting-started/overview`},
    {code: 'pt', label: 'Português', flag: '🇧🇷', to: `${siteBaseUrl}pt/docs/getting-started/overview`},
    {code: 'es', label: 'Español', flag: '🇪🇸', to: `${siteBaseUrl}es/docs/getting-started/overview`},
  ];
  const content = {
    en: {
      tagline: 'A distributed hydrologic-hydrodynamic modeling framework for coupled surface-subsurface processes',
      docsCta: 'Documentation',
      validationCta: 'Validation',
      githubCta: 'GitHub',
      languageLabel: 'Documentation in',
      openLabel: 'Open HydroPol2D in',
      features: [
        {
          title: 'Hydrologic Processes',
          body: 'Interception, evapotranspiration, snow dynamics, infiltration, layered vadose storage, recharge, and groundwater feedbacks.',
        },
        {
          title: 'Hydrodynamic Routing',
          body: 'Local inertial, full momentum, diffusive D4, kinematic D4, cellular automata, and hydraulic controls.',
        },
        {
          title: 'Groundwater Model',
          body: 'Layered recharge, capillary rise, async groundwater scheduling, Boussinesq flow, exfiltration, and saturation excess.',
        },
        {
          title: 'Risk Diagnostics',
          body: 'Human-instability modes 1 and 3 coupled to routed depths and velocities, with explicit validation caveats for diagnostics.',
        },
        {
          title: 'Water Quality',
          body: 'Pollutant buildup, washoff, and distributed transport coupled to surface flow and outlet export.',
        },
      ],
      workflow: {
        eyebrow: 'Integrated process architecture',
        title: 'Model Workflow',
        lead: 'HydroPol2D links atmospheric forcing, canopy interception, vadose-zone storage, groundwater response, dynamic surface routing, pollutant transport, and optional human-instability diagnostics through two-way coupling across the full hydrologic system.',
        forcing: {
          title: 'Atmospheric Forcing',
          subtitle: 'Climate inputs and cryosphere partitioning',
          items: ['Precipitation forcing', 'Snow partition', 'Snowmelt contribution'],
        },
        canopy: {
          title: 'Canopy & Energy Balance',
          subtitle: 'Vegetation controls on effective water input',
          items: ['Interception storage', 'Throughfall / effective rainfall', 'Canopy evaporation and ET losses'],
        },
        coupledCore: {
          title: 'Coupled Core Solver',
          body: 'Exchanges water mass, storage states, and feedbacks across surface, vadose, groundwater, routing, and quality modules.',
        },
        routing: {
          title: 'Surface-Flow Routing',
          subtitle: '2D surface storage, conveyance, and controls',
          items: ['Surface storage and routing', 'Local inertial / full momentum / D4 / CA', 'Reservoirs, BCs, and outlet controls'],
        },
        partitioning: {
          title: 'Surface & Vadose Partitioning',
          subtitle: 'Runoff generation and subsurface allocation',
          items: ['Weighted Darcy infiltration capacity', 'Layered vadose storage dynamics', 'Recharge to groundwater', 'Infiltration excess to surface water depth'],
        },
        groundwater: {
          title: 'Groundwater System',
          subtitle: 'Subsurface storage and return-flow interaction',
          items: ['Async scheduler and capillary rise', '2D Boussinesq groundwater flow', 'Exfiltration to the surface', 'Saturation-excess return flow', 'Feedback to ponded surface depth'],
        },
        quality: {
          title: 'Water-Quality Transport',
          subtitle: 'Constituent generation and surface export',
          items: ['Pollutant buildup', 'Washoff initiation', 'Advection with surface routing', 'Transport and outlet export'],
        },
        summary: ['Atmosphere', 'Land surface forcing', 'Partitioning across runoff, storage, and recharge', 'Subsurface feedback to surface hydraulics', 'Routing-driven constituent export'],
      },
      why: {
        title: 'Why HydroPol2D?',
        lead: 'A modular, high-performance framework for integrated flood, hydrology, groundwater, and water-quality simulation.',
        cards: [
          {
            title: 'Integrated hydrology and hydraulics',
            body: 'Simulate rainfall-runoff generation, layered vadose storage, groundwater feedback, and five routing families in one framework.',
          },
          {
            title: 'Built for large domains',
            body: 'Designed for efficient high-resolution simulations with scalable workflows and advanced numerical options.',
          },
          {
            title: 'Geospatial workflows',
            body: 'Integrates terrain, soil, vegetation, climate, river, and hydraulic-control datasets into a distributed modeling environment.',
          },
          {
            title: 'Open-Source',
            body: 'Flexible for flood inundation, groundwater interaction, green infrastructure, and water-quality applications.',
          },
        ],
      },
      visualAlt: 'HydroPol2D visual',
    },
    pt: {
      tagline: 'Um framework distribuído hidrológico-hidrodinâmico para processos acoplados entre superfície e subsuperfície',
      docsCta: 'Documentação',
      validationCta: 'Validação',
      githubCta: 'GitHub',
      languageLabel: 'Documentação em',
      openLabel: 'Abrir HydroPol2D em',
      features: [
        {
          title: 'Processos Hidrológicos',
          body: 'Interceptação, evapotranspiração, dinâmica de neve, infiltração, armazenamento vadoso em camadas, recarga e feedbacks da água subterrânea.',
        },
        {
          title: 'Roteamento Hidrodinâmico',
          body: 'Local inertial, full momentum, diffusive D4, kinematic D4, cellular automata e controles hidráulicos.',
        },
        {
          title: 'Modelo de Água Subterrânea',
          body: 'Recarga em camadas, ascensão capilar, atualização assíncrona da água subterrânea, fluxo de Boussinesq, exfiltração e excesso de saturação.',
        },
        {
          title: 'Diagnósticos de Risco',
          body: 'Modos 1 e 3 de instabilidade humana acoplados às profundidades e velocidades roteadas, com ressalvas explícitas de validação para diagnósticos.',
        },
        {
          title: 'Qualidade da Água',
          body: 'Acúmulo de poluentes, washoff e transporte distribuído acoplados ao escoamento superficial e à exportação no exutório.',
        },
      ],
      workflow: {
        eyebrow: 'Arquitetura integrada de processos',
        title: 'Fluxo do Modelo',
        lead: 'O HydroPol2D conecta forçantes atmosféricas, interceptação pelo dossel, armazenamento na zona vadosa, resposta da água subterrânea, roteamento superficial dinâmico, transporte de poluentes e diagnósticos opcionais de instabilidade humana por meio de acoplamento bidirecional em todo o sistema hidrológico.',
        forcing: {
          title: 'Forçamento Atmosférico',
          subtitle: 'Entradas climáticas e particionamento da criosfera',
          items: ['Forçamento de precipitação', 'Particionamento da neve', 'Contribuição do derretimento da neve'],
        },
        canopy: {
          title: 'Dossel e Balanço de Energia',
          subtitle: 'Controles da vegetação sobre a entrada efetiva de água',
          items: ['Armazenamento por interceptação', 'Precipitação efetiva / throughfall', 'Evaporação do dossel e perdas por ET'],
        },
        coupledCore: {
          title: 'Núcleo Acoplado de Solução',
          body: 'Troca massa de água, estados de armazenamento e feedbacks entre os módulos de superfície, zona vadosa, água subterrânea, roteamento e qualidade.',
        },
        routing: {
          title: 'Roteamento do Escoamento Superficial',
          subtitle: 'Armazenamento superficial 2D, condução e controles',
          items: ['Armazenamento e roteamento superficial', 'Local inertial / full momentum / D4 / CA', 'Reservatórios, BCs e controles de saída'],
        },
        partitioning: {
          title: 'Particionamento Superfície e Zona Vadosa',
          subtitle: 'Geração de escoamento e alocação subsuperficial',
          items: ['Capacidade de infiltração Darcy ponderada', 'Dinâmica de armazenamento vadoso em camadas', 'Recarga para a água subterrânea', 'Excesso de infiltração convertido em lâmina superficial'],
        },
        groundwater: {
          title: 'Sistema de Água Subterrânea',
          subtitle: 'Armazenamento subsuperficial e interação com fluxo de retorno',
          items: ['Agendador assíncrono e ascensão capilar', 'Fluxo bidimensional de Boussinesq', 'Exfiltração para a superfície', 'Fluxo de retorno por excesso de saturação', 'Feedback para a lâmina superficial acumulada'],
        },
        quality: {
          title: 'Transporte de Qualidade da Água',
          subtitle: 'Geração de constituintes e exportação superficial',
          items: ['Acúmulo de poluentes', 'Início do washoff', 'Advecção com o roteamento superficial', 'Transporte e exportação no exutório'],
        },
        summary: ['Atmosfera', 'Forçamento na superfície terrestre', 'Particionamento entre escoamento, armazenamento e recarga', 'Feedback subsuperficial para a hidráulica de superfície', 'Exportação de constituintes dirigida pelo roteamento'],
      },
      why: {
        title: 'Por que HydroPol2D?',
        lead: 'Um framework modular e de alto desempenho para simulação integrada de inundações, hidrologia, água subterrânea e qualidade da água.',
        cards: [
          {
            title: 'Hidrologia e hidráulica integradas',
            body: 'Simule geração chuva-escoamento, armazenamento vadoso em camadas, feedback da água subterrânea e cinco famílias de roteamento em um único framework.',
          },
          {
            title: 'Preparado para grandes domínios',
            body: 'Projetado para simulações eficientes em alta resolução, com fluxos de trabalho escaláveis e opções numéricas avançadas.',
          },
          {
            title: 'Fluxos geoespaciais',
            body: 'Integra dados de terreno, solo, vegetação, clima, rios e controles hidráulicos em um ambiente de modelagem distribuída.',
          },
          {
            title: 'Código aberto',
            body: 'Flexível para aplicações em inundação, interação com água subterrânea, infraestrutura verde e qualidade da água.',
          },
        ],
      },
      visualAlt: 'Visual do HydroPol2D',
    },
    es: {
      tagline: 'Un marco distribuido hidrológico-hidrodinámico para procesos acoplados entre superficie y subsuperficie',
      docsCta: 'Documentación',
      validationCta: 'Validación',
      githubCta: 'GitHub',
      languageLabel: 'Documentación en',
      openLabel: 'Abrir HydroPol2D en',
      features: [
        {
          title: 'Procesos Hidrológicos',
          body: 'Intercepción, evapotranspiración, dinámica de nieve, infiltración, almacenamiento vadoso en capas, recarga y retroalimentaciones del groundwater.',
        },
        {
          title: 'Enrutamiento Hidrodinámico',
          body: 'Local inertial, full momentum, diffusive D4, kinematic D4, cellular automata y controles hidráulicos.',
        },
        {
          title: 'Modelo de Groundwater',
          body: 'Recarga por capas, ascenso capilar, actualización asíncrona del groundwater, flujo de Boussinesq, exfiltración y exceso de saturación.',
        },
        {
          title: 'Diagnósticos de Riesgo',
          body: 'Modos 1 y 3 de inestabilidad humana acoplados a profundidades y velocidades enrutadas, con advertencias explícitas de validación para los diagnósticos.',
        },
        {
          title: 'Calidad del Agua',
          body: 'Acumulación de contaminantes, washoff y transporte distribuido acoplados al flujo superficial y a la exportación en la salida.',
        },
      ],
      workflow: {
        eyebrow: 'Arquitectura integrada de procesos',
        title: 'Flujo del Modelo',
        lead: 'HydroPol2D conecta forzantes atmosféricos, intercepción del dosel, almacenamiento en la zona vadosa, respuesta del groundwater, enrutamiento superficial dinámico, transporte de contaminantes y diagnósticos opcionales de inestabilidad humana mediante acoplamiento bidireccional en todo el sistema hidrológico.',
        forcing: {
          title: 'Forzamiento Atmosférico',
          subtitle: 'Entradas climáticas y particionamiento de la criosfera',
          items: ['Forzamiento de precipitación', 'Partición de nieve', 'Contribución del deshielo'],
        },
        canopy: {
          title: 'Dosel y Balance de Energía',
          subtitle: 'Controles de la vegetación sobre la entrada efectiva de agua',
          items: ['Almacenamiento por intercepción', 'Precipitación efectiva / throughfall', 'Evaporación del dosel y pérdidas por ET'],
        },
        coupledCore: {
          title: 'Núcleo Acoplado de Solución',
          body: 'Intercambia masa de agua, estados de almacenamiento y retroalimentaciones entre los módulos de superficie, zona vadosa, groundwater, enrutamiento y calidad.',
        },
        routing: {
          title: 'Enrutamiento del Flujo Superficial',
          subtitle: 'Almacenamiento superficial 2D, conducción y controles',
          items: ['Almacenamiento y enrutamiento superficial', 'Local inertial / full momentum / D4 / CA', 'Embalses, BCs y controles de salida'],
        },
        partitioning: {
          title: 'Particionamiento entre Superficie y Zona Vadosa',
          subtitle: 'Generación de escorrentía y asignación subsuperficial',
          items: ['Capacidad de infiltración Darcy ponderada', 'Dinámica de almacenamiento vadoso en capas', 'Recarga al groundwater', 'Exceso de infiltración convertido en lámina superficial'],
        },
        groundwater: {
          title: 'Sistema de Groundwater',
          subtitle: 'Almacenamiento subsuperficial e interacción con flujo de retorno',
          items: ['Programador asíncrono y ascenso capilar', 'Flujo bidimensional de Boussinesq', 'Exfiltración hacia la superficie', 'Flujo de retorno por exceso de saturación', 'Retroalimentación hacia la lámina superficial acumulada'],
        },
        quality: {
          title: 'Transporte de Calidad del Agua',
          subtitle: 'Generación de constituyentes y exportación superficial',
          items: ['Acumulación de contaminantes', 'Inicio del washoff', 'Advección con el enrutamiento superficial', 'Transporte y exportación en la salida'],
        },
        summary: ['Atmósfera', 'Forzamiento en la superficie terrestre', 'Particionamiento entre escorrentía, almacenamiento y recarga', 'Retroalimentación subsuperficial hacia la hidráulica superficial', 'Exportación de constituyentes impulsada por el enrutamiento'],
      },
      why: {
        title: '¿Por qué HydroPol2D?',
        lead: 'Un marco modular y de alto rendimiento para la simulación integrada de inundaciones, hidrología, groundwater y calidad del agua.',
        cards: [
          {
            title: 'Hidrología e hidráulica integradas',
            body: 'Simule generación lluvia-escorrentía, almacenamiento vadoso en capas, retroalimentación del groundwater y cinco familias de enrutamiento en un solo marco.',
          },
          {
            title: 'Diseñado para dominios grandes',
            body: 'Pensado para simulaciones eficientes en alta resolución, con flujos de trabajo escalables y opciones numéricas avanzadas.',
          },
          {
            title: 'Flujos geoespaciales',
            body: 'Integra datos de terreno, suelo, vegetación, clima, ríos y controles hidráulicos en un entorno de modelación distribuida.',
          },
          {
            title: 'Código abierto',
            body: 'Flexible para aplicaciones de inundación, interacción con groundwater, infraestructura verde y calidad del agua.',
          },
        ],
      },
      visualAlt: 'Visual de HydroPol2D',
    },
  }[currentLocale] || null;

  return (
    <Layout title="HydroPol2D">
      {/* HERO */}
    <section className={styles.hero}>
      {/* VIDEO BACKGROUND */}
      <video
        className={styles.heroVideo}
        autoPlay
        loop
        muted
        playsInline
      >
        <source src={useBaseUrl('/videos/flood_video.mp4')} type="video/mp4" />
      </video>

      {/* OPTIONAL DARK OVERLAY */}
      <div className={styles.heroOverlay}></div>

      <div className={styles.heroInner}>
        <img src={logoUrl} alt="HydroPol2D logo" className={styles.heroLogo} />

        <h1>HydroPol2D</h1>
        <p>
          {content.tagline}
        </p>

        <div className={styles.buttons}>
          <Link className="button button--primary button--lg" to={docsUrl}>
            {content.docsCta}
          </Link>
          <Link className="button button--secondary button--lg" to={validationUrl}>
            {content.validationCta}
          </Link>
          <a
            className="button button--secondary button--lg"
            href="https://github.com/marcusnobrega-eng/HydroPol2D"
          >
            {content.githubCta}
          </a>
        </div>

        <div className={styles.languageRow}>
          <span className={styles.languageLabel}>{content.languageLabel}</span>
          <div className={styles.languagePills}>
            {languageOptions.map((language) => (
              <a
                key={language.code}
                href={language.to}
                className={`${styles.languagePill} ${currentLocale === language.code ? styles.languagePillActive : ''}`}
                aria-label={`${content.openLabel} ${language.label}`}
              >
                <span>{language.flag}</span>
                <span>{language.label}</span>
              </a>
            ))}
          </div>
        </div>
      </div>
    </section>

      {/* FEATURES */}
      <section className={styles.features}>
        <div className={styles.grid}>
          <div className={styles.card}>
            <div className={styles.iconWrap}>
              <Droplets size={28} />
            </div>
            <h3>{content.features[0].title}</h3>
            <p>{content.features[0].body}</p>
          </div>

          <div className={styles.card}>
            <div className={styles.iconWrap}>
              <Waves size={28} />
            </div>
            <h3>{content.features[1].title}</h3>
            <p>{content.features[1].body}</p>
          </div>

          <div className={styles.card}>
            <div className={styles.iconWrap}>
              <Mountain size={28} />
            </div>
            <h3>{content.features[2].title}</h3>
            <p>{content.features[2].body}</p>
          </div>

          <div className={styles.card}>
            <div className={styles.iconWrap}>
              <ShieldCheck size={28} />
            </div>
            <h3>{content.features[3].title}</h3>
            <p>{content.features[3].body}</p>
          </div>

          <div className={styles.card}>
            <div className={styles.iconWrap}>
              <FlaskConical size={28} />
            </div>
            <h3>{content.features[4].title}</h3>
            <p>{content.features[4].body}</p>
          </div>
        </div>
      </section>

      {/* WORKFLOW */}
      <section className={styles.workflowPremium}>
        <div className={styles.workflowPremiumInner}>
          <div className={styles.workflowHeader}>
            <div className={styles.workflowEyebrow}>
              <Sparkles size={16} />
              <span>{content.workflow.eyebrow}</span>
            </div>

            <h2>{content.workflow.title}</h2>

            <p className={styles.workflowLead}>{content.workflow.lead}</p>
          </div>

          <div className={styles.workflowStage}>
            <div className={styles.workflowAmbientGlow}></div>

            {/* TOP */}
            <div className={styles.workflowTop}>
              <ProcessCard
                accent="accentSky"
                icon={<CloudRain size={20} />}
                title={content.workflow.forcing.title}
                subtitle={content.workflow.forcing.subtitle}
                items={content.workflow.forcing.items}
              />
            </div>

            {/* MIDDLE LAYER */}
            <div className={styles.workflowMiddle}>
              <ProcessCard
                accent="accentForest"
                icon={<Trees size={20} />}
                title={content.workflow.canopy.title}
                subtitle={content.workflow.canopy.subtitle}
                items={content.workflow.canopy.items}
              />

              <div className={styles.couplingCore}>
                <div className={styles.couplingCoreHalo}></div>
                <div className={styles.couplingCoreInner}>
                  <div className={styles.couplingCoreIcon}>
                    <Orbit size={24} />
                  </div>
                  <h3>{content.workflow.coupledCore.title}</h3>
                  <p>{content.workflow.coupledCore.body}</p>
                </div>
              </div>

              <ProcessCard
                accent="accentBlue"
                icon={<Waves size={20} />}
                title={content.workflow.routing.title}
                subtitle={content.workflow.routing.subtitle}
                items={content.workflow.routing.items}
              />
            </div>

            {/* LOWER LAYER */}
            <div className={styles.workflowBottom}>
              <ProcessCard
                accent="accentAmber"
                icon={<Layers3 size={20} />}
                title={content.workflow.partitioning.title}
                subtitle={content.workflow.partitioning.subtitle}
                items={content.workflow.partitioning.items}
              />

              <ProcessCard
                accent="accentSlate"
                icon={<Mountain size={20} />}
                title={content.workflow.groundwater.title}
                subtitle={content.workflow.groundwater.subtitle}
                items={content.workflow.groundwater.items}
              />

              <ProcessCard
                accent="accentRose"
                icon={<FlaskConical size={20} />}
                title={content.workflow.quality.title}
                subtitle={content.workflow.quality.subtitle}
                items={content.workflow.quality.items}
              />
            </div>

            {/* COUPLING LABELS */}
          </div>

          <div className={styles.workflowSummaryBar}>
            <div className={styles.summaryItem}>
              <CloudSun size={16} />
              <span>{content.workflow.summary[0]}</span>
            </div>

            <ArrowRight size={16} className={styles.summaryArrow} />

            <div className={styles.summaryItem}>
              <Droplets size={16} />
              <span>{content.workflow.summary[1]}</span>
            </div>

            <ArrowRight size={16} className={styles.summaryArrow} />

            <div className={styles.summaryItem}>
              <Layers3 size={16} />
              <span>{content.workflow.summary[2]}</span>
            </div>

            <ArrowRight size={16} className={styles.summaryArrow} />

            <div className={styles.summaryItem}>
              <Mountain size={16} />
              <span>{content.workflow.summary[3]}</span>
            </div>

            <ArrowRight size={16} className={styles.summaryArrow} />

            <div className={styles.summaryItem}>
              <Database size={16} />
              <span>{content.workflow.summary[4]}</span>
            </div>
          </div>
        </div>
      </section>

      {/* WHY SECTION */}
      <section className={styles.whySection}>
        <div className={styles.whyInner}>
          <div className={styles.whyHeader}>
            <h2>{content.why.title}</h2>
            <p>{content.why.lead}</p>
          </div>

          <div className={styles.whyGrid}>
            <div className={`${styles.whyCard} ${styles.whyVisualCard}`}>
              <div className={styles.visualShell}>
                <img
                  src={logoUrl}
                  alt={content.visualAlt}
                  className={styles.visualLogo}
                />
                <div className={styles.visualGlow}></div>
              </div>
            </div>

            <div className={styles.whyCard}>
              <div className={styles.whyIcon}>
                <Gauge size={26} />
              </div>
              <h3>{content.why.cards[0].title}</h3>
              <p>{content.why.cards[0].body}</p>
            </div>

            <div className={styles.whyCard}>
              <div className={styles.whyIcon}>
                <Cpu size={26} />
              </div>
              <h3>{content.why.cards[1].title}</h3>
              <p>{content.why.cards[1].body}</p>
            </div>

            <div className={styles.whyCard}>
              <div className={styles.whyIcon}>
                <Map size={26} />
              </div>
              <h3>{content.why.cards[2].title}</h3>
              <p>{content.why.cards[2].body}</p>
            </div>

            <div className={styles.whyCard}>
              <div className={styles.whyIcon}>
                <ShieldCheck size={26} />
              </div>
              <h3>{content.why.cards[3].title}</h3>
              <p>{content.why.cards[3].body}</p>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
}
