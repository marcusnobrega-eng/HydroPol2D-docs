// @ts-check

import {themes as prismThemes} from 'prism-react-renderer';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'HydroPol2D',
  tagline: 'A distributed hydrologic–hydrodynamic modeling framework',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://marcusnobrega-eng.github.io',
  baseUrl: '/HydroPol2D-docs/',

  organizationName: 'marcusnobrega-eng',
  projectName: 'HydroPol2D-docs',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  stylesheets: [
    {
      href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap',
      type: 'text/css',
    },
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.css',
      type: 'text/css',
    },
  ],

  presets: [
    [
      'classic',
      ({
        docs: {
          sidebarPath: './sidebars.js',
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    ({
      image: 'img/social_card.png',

      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },

      navbar: {
        title: 'HydroPol2D',
        logo: {
          alt: 'HydroPol2D Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Documentation',
          },
          {
            href: 'https://github.com/marcusnobrega-eng/HydroPol2D',
            label: 'Code',
            position: 'right',
          },
        ],
      },

      footer: {},

      docs: {
        sidebar: {
          hideable: true,
          autoCollapseCategories: false,
        },
      },

      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['matlab', 'bash', 'python'],
      },
    }),
};

export default config;