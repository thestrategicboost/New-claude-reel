export type Tab = 'projet' | 'effets' | 'looks' | 'charte'

declare module 'claude-code' {
  interface PluginState {
    'studio-montage': { tab: Tab; cat: number }
  }
}
