import { defineManifest } from '@crxjs/vite-plugin'
import pkg from './package.json'

export default defineManifest({
  manifest_version: 3,
  name: pkg.name,
  version: pkg.version,
  icons: {
    48: 'public/logo.png',
  },
  action: {
    default_icon: {
      48: 'public/logo.png',
    },
    default_popup: 'src/popup/index.html',
  },
  permissions: ['scripting', 'activeTab'],
  host_permissions: ['https://www.youtube.com/*'],
  content_scripts: [
    {
      js: ['src/content/main.tsx'],
      matches: ['https://www.youtube.com/*'],
      run_at: 'document_idle',
    },
  ],
})
