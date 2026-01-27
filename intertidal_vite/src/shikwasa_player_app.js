import './assets/shikwasa_player.scss'
import { Player, Chapter } from 'shikwasa'

Player.use(Chapter)

const shikwasaPlayers = []
const mountElList = document.querySelectorAll('.shikwasa-player-app')
mountElList.forEach((mountEl) => {
  shikwasaPlayers.push(new Player({
    container: mountEl,
    audio: {
      // {src, title, artist, cover, }
      ...mountEl.dataset,
      chapters: mountEl.dataset.chaptersJson ? JSON.parse(mountEl.dataset.chaptersJson) : [],
    },
    theme: 'dark',
    themeColor: 'rgb(85,185,243)',
    fixed: {
      type: 'static',
    },
    autoplay: false,
    muted: false,
    preload: 'metadata',
    download: true,
  }))
})
