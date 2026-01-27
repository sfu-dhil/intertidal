import './assets/aplayer.scss'
import APlayer from 'aplayer'


const aPlayers = []
const mountElList = document.querySelectorAll('.aplayer-app')
mountElList.forEach((mountEl) => {
  const audio = mountEl.dataset.audioJson ? JSON.parse(mountEl.dataset.audioJson) : []
  aPlayers.push(new APlayer({
    container: mountEl,
    audio: audio,
    autoplay: false,
    // theme: '#b7daff',
    loop: 'all',
    order: 'list',
    preload: 'metadata',
    volume: 0.5, //default, remember's user setting
    listFolded: audio.length > 1 ? false : true, // only hide the playlist if there is one or zero audio files
    listMaxHeight: '10em',
  }))
})
