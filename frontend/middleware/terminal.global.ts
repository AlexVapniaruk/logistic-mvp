export default defineNuxtRouteMiddleware((to) => {
  if (import.meta.server) return
  // Terminal picker and its sub-routes are always allowed
  if (to.path === '/terminals' || to.path.startsWith('/terminals/')) return

  const terminalsStore = useTerminalsStore()

  if (!terminalsStore.selected) {
    // Try to restore from localStorage
    const savedId = localStorage.getItem('selectedTerminalId')
    if (savedId && terminalsStore.items.length) {
      const found = terminalsStore.items.find(t => t.id === Number(savedId))
      if (found) {
        terminalsStore.selectTerminal(found)
        return
      }
    }
    return navigateTo('/terminals')
  }
})
