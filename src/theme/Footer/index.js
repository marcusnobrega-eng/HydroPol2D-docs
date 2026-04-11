import React from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import {
  FaGithub,
  FaLinkedin,
  FaYoutube,
  FaInstagram,
} from 'react-icons/fa';
import {
  SiGooglescholar,
  SiOrcid,
  SiResearchgate,
} from 'react-icons/si';
import styles from './styles.module.css';

function HydroBackground() {
  return (
    <div className={styles.hydroBg} aria-hidden="true">
      <svg
        className={styles.hydroSvg}
        viewBox="0 0 1600 500"
        preserveAspectRatio="none"
      >
        {/* BANK ENVELOPE (top) */}
        <path
          d="M-100 200
             C 150 170, 400 210, 700 240
             S 1100 190, 1500 220
             S 1700 250, 1800 240"
          className={styles.bankSoft}
        />

        {/* BANK ENVELOPE (bottom) */}
        <path
          d="M-100 370
             C 150 340, 400 380, 700 410
             S 1100 360, 1500 390
             S 1700 420, 1800 410"
          className={styles.bankSoft}
        />

        {/* FLOW LAYERS */}
        <path
          d="M-80 235
             C 180 205, 420 245, 720 275
             S 1120 225, 1520 255
             S 1700 285, 1780 275"
          className={styles.mainFlux1}
        />

        <path
          d="M-80 265
             C 180 235, 420 275, 720 305
             S 1120 255, 1520 285
             S 1700 315, 1780 305"
          className={styles.mainFlux2}
        />

        {/* THALWEG */}
        <path
          d="M-80 295
             C 180 255, 420 295, 720 325
             S 1120 275, 1520 305
             S 1700 335, 1780 325"
          className={styles.thalweg}
        />

        <path
          d="M-80 325
             C 180 295, 420 335, 720 365
             S 1120 315, 1520 345
             S 1700 375, 1780 365"
          className={styles.mainFlux3}
        />

        {/* SECONDARY FLOW */}
        <path
          d="M-100 355
             C 180 325, 440 365, 760 395
             S 1160 345, 1560 375
             S 1700 405, 1780 395"
          className={styles.secondaryFlux}
        />

        {/* PARTICLES */}
        <path
          d="M100 295
             C 420 275, 760 315, 1200 300
             S 1500 305, 1600 300"
          className={styles.particleTrack}
        />

        <path
          d="M200 320
             C 520 300, 860 340, 1300 325
             S 1550 330, 1650 325"
          className={styles.particleTrack2}
        />
      </svg>

      <div className={styles.gridGlow}></div>
    </div>
  );
}

export default function Footer() {
  const logoUrl = useBaseUrl('/img/logo.svg');

  return (
    <footer className={styles.footer}>
      <div className={styles.background}></div>
      <HydroBackground />

      <div className={styles.inner}>
        <div className={styles.left}>
          <div className={styles.brandRow}>
            <img
              src={logoUrl}
              alt="HydroPol2D logo"
              className={styles.logo}
            />
            <span className={styles.brandName}>HydroPol2D</span>
          </div>

          <p className={styles.copy}>
            A distributed hydrologic–hydrodynamic framework for coupled
            surface–subsurface processes.
          </p>

          <span className={styles.copyright}>
            © {new Date().getFullYear()} HydroPol2D
          </span>
        </div>

        <div className={styles.right}>
          <div className={styles.socials}>
            {/* GitHub */}
            <a
              href="https://github.com/marcusnobrega-eng/HydroPol2D"
              className={styles.icon}
              aria-label="GitHub"
              target="_blank"
              rel="noopener noreferrer"
              title="GitHub"
            >
              <FaGithub size={20} />
            </a>

            {/* LinkedIn */}
            <a
              href="https://www.linkedin.com/in/marcus-n%C3%B3brega-744b61138/"
              className={styles.icon}
              aria-label="LinkedIn"
              target="_blank"
              rel="noopener noreferrer"
              title="LinkedIn"
            >
              <FaLinkedin size={20} />
            </a>

            {/* Google Scholar */}
            <a
              href="https://scholar.google.com/scholar?q=Marcus+N%C3%B3brega"
              className={styles.icon}
              aria-label="Google Scholar"
              target="_blank"
              rel="noopener noreferrer"
              title="Google Scholar"
            >
              <SiGooglescholar size={20} />
            </a>

            {/* ResearchGate */}
            <a
              href="https://www.researchgate.net/profile/Marcus-Gomes-Jr"
              className={styles.icon}
              aria-label="ResearchGate"
              target="_blank"
              rel="noopener noreferrer"
              title="ResearchGate"
            >
              <SiResearchgate size={20} />
            </a>

            {/* ORCID */}
            <a
              href="https://orcid.org/0000-0002-8250-8195"
              className={styles.icon}
              aria-label="ORCID"
              target="_blank"
              rel="noopener noreferrer"
              title="ORCID"
            >
              <SiOrcid size={20} />
            </a>

            {/* YouTube */}
            <a
              href="#"
              className={styles.icon}
              aria-label="YouTube"
              target="_blank"
              rel="noopener noreferrer"
              title="YouTube"
            >
              <FaYoutube size={20} />
            </a>

            {/* Instagram */}
            <a
              href="#"
              className={styles.icon}
              aria-label="Instagram"
              target="_blank"
              rel="noopener noreferrer"
              title="Instagram"
            >
              <FaInstagram size={20} />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}