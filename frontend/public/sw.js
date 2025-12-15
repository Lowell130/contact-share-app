// Empty service worker to satisfy browser requests and prevent 404 errors
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', () => self.clients.claim());
