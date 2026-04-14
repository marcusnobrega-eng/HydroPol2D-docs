// @ts-check

/**
 * @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: ['getting-started/overview'],
    },
    {
      type: 'category',
      label: 'Inputs',
      items: [
        'inputs/overview',
        'inputs/dem',
        'inputs/lulc',
        'inputs/soil',
        'inputs/dtb',
        'inputs/lai',
        'inputs/albedo',
        'inputs/parameter-tables',
        'inputs/optional-forcing',
      ],
    },
    {
      type: 'category',
      label: 'Configuration',
      items: [
        'configuration/overview',
        'configuration/general_data',
        'configuration/flags',
      ],
    },
    {
      type: 'category',
      label: 'GEE Codes',
      items: [
        'GEE/overview',
        'GEE/DailyForcing',
        'GEE/GPM',
        'GEE/python_hp2d'
      ],
    },
    {
    type: 'category',
    label: 'Background/Theory',
    items: [
      'theory/overview',
      'theory/hydrologic-model',
      'theory/hydrodynamic-model',
      'theory/water-quality-model',
      'theory/groundwater-model',
    ],
  },
  ],
};

export default sidebars;