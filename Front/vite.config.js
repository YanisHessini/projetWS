import { fileURLToPath, URL } from 'url'

import { defineConfig } from 'vite'
import analyze from 'rollup-plugin-analyzer'
import autoImport from 'unplugin-auto-import/vite'
import components from 'unplugin-vue-components/vite'
import favicons from '@darkobits/vite-plugin-favicons'
import icons from 'unplugin-icons/vite'
import iconsResolver from 'unplugin-icons/resolver'
import pages from 'vite-plugin-pages'
import svgLoader from 'vite-svg-loader'
import sw from 'vite-plugin-sw'
import vue from '@vitejs/plugin-vue'

import autoprefixer from 'autoprefixer'
import tailwindcss from 'tailwindcss'

import packageJSON from './package.json'

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '/src': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  plugins: [
    vue(),

    // https://github.com/hannoeru/vite-plugin-pages
    pages({
      exclude: ['**/components/*.vue'],
    }),

    // https://github.com/antfu/unplugin-auto-import
    autoImport({
      imports: ['vue', '@vueuse/core', '@vueuse/head', 'vue-router'],
      dts: './src/auto-imports.d.ts',
    }),

    // https://github.com/antfu/unplugin-vue-components
    components({
      dirs: [],
      resolvers: [
        // https://github.com/antfu/vite-plugin-icons
        iconsResolver({
          componentPrefix: 'Icon',
        }),
      ],
      dts: './src/components.d.ts',
    }),

    // https://github.com/antfu/vite-plugin-icons
    icons({
      autoInstall: true,
    }),

    svgLoader(),

    // sw({
    //   verbose: true,
    // }),

    favicons({
      cache: false, // until plugin is fixed
      appName:
        packageJSON.name.charAt(0).toUpperCase() + packageJSON.name.slice(1),
      appDescription: packageJSON.description,
      icons: {
        // android: {
        //   source: './src/assets/svg/mapview/logo.svg',
        //   background: faviconBackground,
        //   offset: faviconOffset,
        // },
        // appleIcon: {
        //   source: './src/assets/svg/mapview/logo.svg',
        //   offset: faviconOffset,
        // },
        // appleStartup: {
        //   source: './src/assets/svg/mapview/logoFull.svg',
        //   offset: faviconOffset * 2,
        // },
        // favicons: {
        //   source: './src/assets/svg/mapview/logo.svg',
        //   offset: faviconOffset,
        // },
      },
    }),

    analyze({
      summaryOnly: true,
    }),
  ],
	server: {
    watch: {
      usePolling: true
    }
  },
  css: {
    postcss: {
      plugins: [autoprefixer(), tailwindcss()],
    },
  },
})
