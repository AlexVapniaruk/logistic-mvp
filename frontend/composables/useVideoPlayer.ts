import { ref, onUnmounted } from 'vue'

export function useVideoPlayer() {
  const videoRef = ref<HTMLVideoElement | null>(null)
  const isPlaying = ref(false)
  const currentTime = ref(0)

  let interval: ReturnType<typeof setInterval> | null = null

  function play(): void {
    videoRef.value?.play()
    isPlaying.value = true
    interval = setInterval(() => {
      currentTime.value = videoRef.value?.currentTime ?? 0
    }, 250)
  }

  function pause(): void {
    videoRef.value?.pause()
    isPlaying.value = false
    if (interval) clearInterval(interval)
  }

  function seekTo(seconds: number): void {
    if (videoRef.value) {
      videoRef.value.currentTime = seconds
      currentTime.value = seconds
    }
  }

  onUnmounted(() => {
    if (interval) clearInterval(interval)
  })

  return { videoRef, isPlaying, currentTime, play, pause, seekTo }
}
