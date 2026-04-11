import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
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
  const logoUrl = useBaseUrl('/img/logo.svg');

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
          A distributed hydrologic-hydrodynamic modeling framework for coupled
          surface-subsurface processes
        </p>

        <div className={styles.buttons}>
          <Link className="button button--primary button--lg" to="/docs/getting-started/overview">
            Documentation
          </Link>
          <a
            className="button button--secondary button--lg"
            href="https://github.com/marcusnobrega-eng/HydroPol2D"
          >
            GitHub
          </a>
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
            <h3>Hydrologic Processes</h3>
            <p>
              Interception, evapotranspiration, snow dynamics, infiltration,
              vadose storage, recharge, and groundwater feedbacks.
            </p>
          </div>

          <div className={styles.card}>
            <div className={styles.iconWrap}>
              <Waves size={28} />
            </div>
            <h3>Hydrodynamic Routing</h3>
            <p>
              Local inertial routing with multiple numerical schemes, optional
              cellular automata routing, and hydraulic controls.
            </p>
          </div>

          <div className={styles.card}>
            <div className={styles.iconWrap}>
              <Mountain size={28} />
            </div>
            <h3>Groundwater Model</h3>
            <p>
              Recharge coupling, 2D Boussinesq groundwater flow, exfiltration,
              and saturation-excess return flow.
            </p>
          </div>

          <div className={styles.card}>
            <div className={styles.iconWrap}>
              <FlaskConical size={28} />
            </div>
            <h3>Water Quality</h3>
            <p>
              Pollutant buildup, washoff, and distributed transport coupled to
              surface flow and outlet export.
            </p>
          </div>
        </div>
      </section>

      {/* WORKFLOW */}
      <section className={styles.workflowPremium}>
        <div className={styles.workflowPremiumInner}>
          <div className={styles.workflowHeader}>
            <div className={styles.workflowEyebrow}>
              <Sparkles size={16} />
              <span>Integrated process architecture</span>
            </div>

            <h2>Model Workflow</h2>

            <p className={styles.workflowLead}>
              HydroPol2D links atmospheric forcing, canopy interception, vadose-zone
              storage, groundwater response, dynamic surface routing, and pollutant
              transport through two-way coupling across the full hydrologic system.
            </p>
          </div>

          <div className={styles.workflowStage}>
            <div className={styles.workflowAmbientGlow}></div>

            {/* TOP */}
            <div className={styles.workflowTop}>
              <ProcessCard
                accent="accentSky"
                icon={<CloudRain size={20} />}
                title="Atmospheric Forcing"
                subtitle="Climate inputs and cryosphere partitioning"
                items={[
                  'Precipitation forcing',
                  'Snow partition',
                  'Snowmelt contribution',
                ]}
              />
            </div>

            {/* MIDDLE LAYER */}
            <div className={styles.workflowMiddle}>
              <ProcessCard
                accent="accentForest"
                icon={<Trees size={20} />}
                title="Canopy & Energy Balance"
                subtitle="Vegetation controls on effective water input"
                items={[
                  'Interception storage',
                  'Throughfall / effective rainfall',
                  'Canopy evaporation and ET losses',
                ]}
              />

              <div className={styles.couplingCore}>
                <div className={styles.couplingCoreHalo}></div>
                <div className={styles.couplingCoreInner}>
                  <div className={styles.couplingCoreIcon}>
                    <Orbit size={24} />
                  </div>
                  <h3>Coupled Core Solver</h3>
                  <p>
                    Exchanges water mass, storage states, and feedbacks across
                    surface, vadose, groundwater, routing, and quality modules.
                  </p>
                </div>
              </div>

              <ProcessCard
                accent="accentBlue"
                icon={<Waves size={20} />}
                title="Surface-Flow Routing"
                subtitle="2D surface storage, conveyance, and controls"
                items={[
                  'Surface storage and routing',
                  'Local inertial / CA solver',
                  'Reservoirs, BCs, and outlet controls',
                ]}
              />
            </div>

            {/* LOWER LAYER */}
            <div className={styles.workflowBottom}>
              <ProcessCard
                accent="accentAmber"
                icon={<Layers3 size={20} />}
                title="Surface & Vadose Partitioning"
                subtitle="Runoff generation and subsurface allocation"
                items={[
                  'Infiltration capacity',
                  'Vadose storage dynamics',
                  'Recharge to groundwater',
                  'Infiltration excess to surface water depth',
                ]}
              />

              <ProcessCard
                accent="accentSlate"
                icon={<Mountain size={20} />}
                title="Groundwater System"
                subtitle="Subsurface storage and return-flow interaction"
                items={[
                  '2D Boussinesq groundwater flow',
                  'Exfiltration to the surface',
                  'Saturation-excess return flow',
                  'Feedback to ponded surface depth',
                ]}
              />

              <ProcessCard
                accent="accentRose"
                icon={<FlaskConical size={20} />}
                title="Water-Quality Transport"
                subtitle="Constituent generation and surface export"
                items={[
                  'Pollutant buildup',
                  'Washoff initiation',
                  'Advection with surface routing',
                  'Transport and outlet export',
                ]}
              />
            </div>

            {/* COUPLING LABELS */}
          </div>

          <div className={styles.workflowSummaryBar}>
            <div className={styles.summaryItem}>
              <CloudSun size={16} />
              <span>Atmosphere</span>
            </div>

            <ArrowRight size={16} className={styles.summaryArrow} />

            <div className={styles.summaryItem}>
              <Droplets size={16} />
              <span>Land surface forcing</span>
            </div>

            <ArrowRight size={16} className={styles.summaryArrow} />

            <div className={styles.summaryItem}>
              <Layers3 size={16} />
              <span>Partitioning across runoff, storage, and recharge</span>
            </div>

            <ArrowRight size={16} className={styles.summaryArrow} />

            <div className={styles.summaryItem}>
              <Mountain size={16} />
              <span>Subsurface feedback to surface hydraulics</span>
            </div>

            <ArrowRight size={16} className={styles.summaryArrow} />

            <div className={styles.summaryItem}>
              <Database size={16} />
              <span>Routing-driven constituent export</span>
            </div>
          </div>
        </div>
      </section>

      {/* WHY SECTION */}
      <section className={styles.whySection}>
        <div className={styles.whyInner}>
          <div className={styles.whyHeader}>
            <h2>Why HydroPol2D?</h2>
            <p>
              A modular, high-performance framework for integrated flood,
              hydrology, groundwater, and water-quality simulation.
            </p>
          </div>

          <div className={styles.whyGrid}>
            <div className={`${styles.whyCard} ${styles.whyVisualCard}`}>
              <div className={styles.visualShell}>
                <img
                  src={logoUrl}
                  alt="HydroPol2D visual"
                  className={styles.visualLogo}
                />
                <div className={styles.visualGlow}></div>
              </div>
            </div>

            <div className={styles.whyCard}>
              <div className={styles.whyIcon}>
                <Gauge size={26} />
              </div>
              <h3>Integrated hydrology and hydraulics</h3>
              <p>
                Simulate rainfall-runoff generation, vadose storage, groundwater feedback,
                and dynamic surface routing in one framework.
              </p>
            </div>

            <div className={styles.whyCard}>
              <div className={styles.whyIcon}>
                <Cpu size={26} />
              </div>
              <h3>Built for large domains</h3>
              <p>
                Designed for efficient high-resolution simulations with scalable workflows
                and advanced numerical options.
              </p>
            </div>

            <div className={styles.whyCard}>
              <div className={styles.whyIcon}>
                <Map size={26} />
              </div>
              <h3>Geospatial workflows</h3>
              <p>
                Integrates terrain, soil, vegetation, climate, river, and hydraulic-control
                datasets into a distributed modeling environment.
              </p>
            </div>

            <div className={styles.whyCard}>
              <div className={styles.whyIcon}>
                <ShieldCheck size={26} />
              </div>
              <h3>Open-Source</h3>
              <p>
                Flexible for flood inundation, groundwater interaction, green infrastructure,
                and water-quality applications.
              </p>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
}