import { onUnmounted } from 'vue'
import { WsClient } from '~/api-sdk/ws.client'
import type { WsMessage, WsMessageType } from '~/api-sdk/types'

export function useWebSocket(path: string) {
  const config = useRuntimeConfig()
  const wsBase = (config.public.wsBase as string | undefined) ?? 'ws://localhost:8000'
  const client = new WsClient({ url: `${wsBase}${path}` })

  client.connect()
  onUnmounted(() => client.disconnect())

  function on(type: WsMessageType | '*', handler: (msg: WsMessage) => void) {
    return client.on(type, handler)
  }

  return { on }
}
