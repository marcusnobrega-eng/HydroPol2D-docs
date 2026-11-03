// @ts-check

/**
 * @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        'getting-started/overview',
        'getting-started/model-building-workflow',
        'getting-started/excel-workflow',
        'getting-started/ecosystem-architecture',
      ],
    },
    {
      type: 'category',
      label: 'Studio',
      items: [
        'studio/overview',
        'studio/install-and-license',
        'studio/building-a-model',
        'studio/working-in-studio',
        'studio/run-and-results',
        'studio/calibrate',
      ],
    },
    {
      type: 'category',
      label: 'Case Builder',
      items: [
        'builder/overview',
      ],
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
        'inputs/additional-spatial-inputs',
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
      label: 'Calibration',
      items: ['calibration/ga-calibration', 'calibration/groundwater-recession'],
    },
    {
      type: 'category',
      label: 'Validation',
      items: [
        'validation/overview',
        'validation/validation-status',
        'validation/hydrologic-modules',
        'validation/groundwater-recharge',
        {
          type: 'category',
          label: 'Hydrodynamics and Routing',
          link: {
            type: 'doc',
            id: 'validation/hydrodynamics-routing',
          },
          items: ['validation/neal-subgrid', 'validation/voronoi-mesh'],
        },
        'validation/ancillary-modules',
        'validation/limitations',
        'validation/changelog',
      ],
    },
    {
      type: 'category',
      label: 'Google Earth Engine',
      items: [
        'GEE/overview',
        'GEE/DailyForcing',
        'GEE/GPM'
      ],
    },
    {
      type: 'category',
      label: 'Examples',
      items: [
        'Examples/RainfallRunoff'
      ],
    },
    {
    type: 'category',
    label: 'Theory',
    items: [
      'theory/overview',
      'theory/hydrologic-model',
      'theory/groundwater-model',
      'theory/layered-subsurface',
      'theory/hydrodynamic-model',
      'theory/human-instability',
      'theory/water-quality-model',
    ],
  },
  ],
};

export default sidebars;
