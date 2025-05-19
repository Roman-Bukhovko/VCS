// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/init': 'http://localhost:5000',
      '/status': 'http://localhost:5000',
      '/log': 'http://localhost:5000',
      '/commit': 'http://localhost:5000',
      '/add': 'http://localhost:5000',
      '/restore': 'http://localhost:5000',
      '/stash': 'http://localhost:5000',
      '/stash/pop': 'http://localhost:5000',
      '/current-branch': 'http://localhost:5000',
      '/branch': 'http://localhost:5000',
      '/checkout-branch': 'http://localhost:5000',
      '/merge': 'http://localhost:5000',
      '/revert': 'http://localhost:5000',
      '/push': 'http://localhost:5000',
      '/pull': 'http://localhost:5000'
    }
  }
});
