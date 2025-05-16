import { defineConfig } from 'vite';
import vitePrerender from 'vite-plugin-prerender';

import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue(),
  vitePrerender({
    staticDir: path.join(__dirname, 'build'),
    routes: ['/', '/about-us', '/sign-in', '/sign-up', '/account']
  })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  base: "/",
  build: {
    outDir: './build'
  }
});
