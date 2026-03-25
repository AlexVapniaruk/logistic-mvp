import type { WsMessage, WsMessageType } from './types'

type MessageHandler = (message: WsMessage) => void

interface WsClientOptions {
  url: string
  reconnectDelayMs?: number
  maxReconnectAttempts?: number
}

export class WsClient {
  private ws: WebSocket | null = null
  private handlers = new Map<WsMessageType | '*', Set<MessageHandler>>()
  private reconnectAttempts = 0
  private readonly options: Required<WsClientOptions>

  constructor(options: WsClientOptions) {
    this.options = {
      reconnectDelayMs: 3000,
      maxReconnectAttempts: 5,
      ...options,
    }
  }

  connect(): void {
    this.ws = new WebSocket(this.options.url)
    this.ws.onmessage = (event) => this.handleMessage(event)
    this.ws.onclose = () => this.handleClose()
    this.ws.onerror = (error) => console.error('[WsClient] error', error)
    this.ws.onopen = () => {
      this.reconnectAttempts = 0
    }
  }

  on(type: WsMessageType | '*', handler: MessageHandler): () => void {
    if (!this.handlers.has(type)) this.handlers.set(type, new Set())
    this.handlers.get(type)!.add(handler)
    return () => this.handlers.get(type)?.delete(handler)
  }

  disconnect(): void {
    this.ws?.close()
    this.ws = null
  }

  private handleMessage(event: MessageEvent): void {
    const message: WsMessage = JSON.parse(event.data as string)
    this.handlers.get(message.type)?.forEach((h) => h(message))
    this.handlers.get('*')?.forEach((h) => h(message))
  }

  private handleClose(): void {
    if (this.reconnectAttempts >= this.options.maxReconnectAttempts) return
    this.reconnectAttempts++
    setTimeout(() => this.connect(), this.options.reconnectDelayMs)
  }
}
