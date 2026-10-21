import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Tab } from '../types'

// Maé's editing studio: a pane beside the chat with her projects, her 59 named effects (video-edit skill,
// references/effects.md), her looks and her brand charte. Every button writes a ready request in the prompt box
// (she completes it and sends), the quick ones send it straight away.

const PANE = 'studio'
const TITLE = '🎬 Studio montage'
const tab = atom({ plugin: 'studio-montage', key: 'tab' } as const, 'projet' as Tab)
const cat = atom({ plugin: 'studio-montage', key: 'cat' } as const, 0)

const BROWN = '#8C5C41'
const GOLD = '#D6AE66'

const TABS: [Tab, string][] = [['projet', 'Projet'], ['effets', 'Effets'], ['looks', 'Looks'], ['charte', 'Ma charte']]

const EFFECTS: [string, [number, string, string][]][] = [
  ['Textes', [
    [1, 'Kinetic hook', 'accroche en gros blocs'], [2, 'Gravity drop', 'lettres qui tombent'], [3, 'Giant captions', 'mot géant'],
    [13, 'Title card', 'carte titre'], [53, 'Depth scatter', 'mots en profondeur'], [54, 'Stat stack', 'gros chiffre'],
    [39, 'Odometer', 'compteur qui défile'], [48, 'Scene text', 'mots sur le mur'], [49, 'Neon sign', 'néon derrière moi'],
    [32, 'Glass type', 'mot en verre'], [31, 'Cover story', 'couverture magazine'], [46, 'Word pile', 'mots empilés'],
    [56, 'Chip row', 'pastilles sous les sous-titres'], [55, 'Dot counter', 'points 1/3'],
  ]],
  ['Interfaces', [
    [4, 'Prompt bar', 'barre de prompt'], [5, 'Storyboard deck', 'éventail de réels'], [6, 'Icon strike', 'logo barré'],
    [7, 'File drop', 'dépôt de fichier'], [8, 'NLE timeline', 'timeline de montage'], [9, 'Jiggle delete', 'appli supprimée'],
    [42, 'Timeline burn', 'timeline qui brûle'], [58, 'Phone mockup', 'téléphone 3D'], [21, 'UI world', 'fond appli'],
    [45, 'Code scan', 'image en code'], [57, 'Serif flow', 'étapes du process'], [34, 'The stack', 'cartes de stats'],
    [50, 'Spatial glass', 'panneaux en verre'],
  ]],
  ['Réseaux', [
    [14, 'Playing grid', 'grille de réels'], [15, 'Reel feed', 'fil de réels'], [16, 'Video card', 'carte vidéo'],
    [17, 'Comment CTA', 'commente MOT'], [18, 'Comment drop', 'commentaires qui tombent'], [59, 'Comment bubble', 'commentaire + réponse'],
    [20, 'Couch wall', 'mur de réels'], [24, 'Headline wall', 'articles au mur'],
  ]],
  ['Derrière moi', [
    [19, 'Orbit', 'logos en orbite'], [33, 'Clone', 'mes clones'], [36, 'Spotlight', 'projecteur'], [52, 'God rays', 'rayons de lumière'],
    [43, 'Knockout tiles', 'tuiles qui tombent'], [47, 'Inside out', 'fenêtre dans ma silhouette'], [27, 'Green screen', 'fond remplacé'],
    [30, 'Vertigo', 'effet vertige'], [22, 'Frame break', 'je sors du cadre'], [26, 'Chart grow', 'courbe qui monte'],
  ]],
  ['Image & cuts', [
    [10, 'Grade slider', 'avant / après'], [11, 'Eyedropper grade', 'pipette couleur'], [12, 'Film look', 'look film'],
    [23, 'Digital zoom', 'zoom sur moi'], [25, 'Zoom-through cut', 'transition zoom'], [41, 'Blackout', 'écran noir'],
    [44, 'Shatter 3D', 'image qui éclate'], [51, 'Rack focus', 'mise au point'],
  ]],
  ['Fun', [
    [28, 'Paper cut', 'collage papier'], [29, 'Doodle boil', 'dessins à la main'], [35, 'Sticky text', 'sticker sur moi'],
    [37, 'Freeze and label', 'arrêt sur image + flèches'], [38, 'Pointer callout', 'cartes reliées à moi'], [40, 'Freeze sticker', 'moi en sticker'],
  ]],
]

const LOOKS: [string, string][] = [
  ['Lilas / rosé', 'mon look lilas rosé habituel'], ['Naturel', 'un look naturel, sans filtre fort'],
  ['Moody', 'un look moody, plus sombre et contrasté'], ['Doré doux', 'un look doré légèrement chaud'],
]

const fill = ($: any, text: string) => $.prompt.fill({ text, mode: 'replace' })
const send = ($: any, text: string) => $.prompt.submit({ text })

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'studio', description: 'Ouvre le panneau Studio montage' })
    $.ui.status('🎬 Studio montage · claude.ai/artifact/7q1vQWhsMpfhFBbWs7TVpD')

    return next(e)
  })

  on('command.run', { command: 'studio' }, async $ => {
    await $.ui.open({ id: PANE, title: TITLE })

    return { text: 'Studio montage ouvert.' }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text, Button } = $.ui.resolve(e)
    const t = await read($, tab)
    const c = await read($, cat)
    const go = (v: Tab) => () => void update($, tab, () => v)

    const head = (
      <Box flexDirection="column" marginBottom={1}>
        <Text bold color={BROWN}>STUDIO MONTAGE</Text>
        <Text dimColor>thestrategicboost.fr · tes réels avec Claude</Text>
        <Box flexDirection="row" flexWrap="wrap" gap={1} marginTop={1}>
          {TABS.map(([v, name]) => (
            <Button key={`tab-${v}`} variant={t === v ? 'primary' : 'secondary'} onPress={go(v)}>{name}</Button>
          ))}
        </Box>
      </Box>
    )

    let body
    if (t === 'projet') {
      body = (
        <Box flexDirection="column" gap={1}>
          <Text bold>Nouveau projet</Text>
          <Button key="new" variant="primary" onPress={() => void fill($,
            "Monte ma nouvelle vidéo avec le skill video-edit.\nMes rushs : [colle le lien Google Drive]\nMon inspiration : [colle le lien du réel]\nCe que je veux : [décris en une phrase]\nFais d'abord un test en images.")}>
            ✚ Nouveau montage
          </Button>
          <Button key="inspi" onPress={() => void fill($,
            'Regarde ce réel et ajoute ses effets à mon skill, puis fais un test : [colle le lien]')}>
            ✦ Ajouter les effets d'un réel
          </Button>
          <Text bold>Le montage en cours</Text>
          <Button key="test" onPress={() => void send($, 'Envoie-moi un test en images de la vidéo en cours.')}>🧪 Envoie-moi un test</Button>
          <Button key="final" onPress={() => void send($, 'Envoie-moi la vidéo finale en haute qualité, prête à poster.')}>📤 Vidéo finale</Button>
          <Button key="change" onPress={() => void fill($, 'Dans la vidéo en cours, change : ')}>✎ Demander une modification</Button>
          <Button key="da" onPress={() => void fill($,
            "Refais une nouvelle DA de la vidéo [nom] pour la republier en réel d'essai : change les écritures, les effets, les encarts, tout. Envoie-moi un test d'abord.")}>
            ↻ Nouvelle DA (réel d'essai)
          </Button>
          <Button key="cover" onPress={() => void fill($, 'Fais-moi une couverture pour la vidéo [nom], dans ma charte.')}>▣ Couverture du réel</Button>
        </Box>
      )
    } else if (t === 'effets') {
      const list = (EFFECTS[c] ?? EFFECTS[0])?.[1] ?? []
      body = (
        <Box flexDirection="column" gap={1}>
          <Box flexDirection="row" flexWrap="wrap" gap={1}>
            {EFFECTS.map(([name], i) => (
              <Button key={`cat-${i}`} variant={i === c ? 'primary' : 'secondary'} onPress={() => void update($, cat, () => i)}>{name}</Button>
            ))}
          </Box>
          <Text dimColor>Appuie sur un effet : la demande s'écrit, tu complètes le mot et tu envoies.</Text>
          {list.map(([num, name, fr]) => (
            <Button key={`fx-${num}`} plain onPress={() => void fill($,
              `Ajoute l'effet ${name} (n°${num}) dans ma vidéo en cours, sur le mot « [mot] ». Envoie-moi un test d'abord.`)}>
              <Text color={GOLD}>{String(num).padStart(2, '0')} </Text>{name} <Text dimColor>· {fr}</Text>
            </Button>
          ))}
        </Box>
      )
    } else if (t === 'looks') {
      body = (
        <Box flexDirection="column" gap={1}>
          <Text dimColor>Change la couleur de toute la vidéo en cours :</Text>
          {LOOKS.map(([name, desc]) => (
            <Button key={`look-${name}`} onPress={() => void fill($, `Applique ${desc} à toute la vidéo en cours et envoie-moi un test.`)}>{name}</Button>
          ))}
          <Button key="look-compare" onPress={() => void send($, 'Montre-moi 2 options de couleur pour la vidéo en cours, côte à côte.')}>Comparer 2 options</Button>
        </Box>
      )
    } else {
      body = (
        <Box flexDirection="column" gap={1}>
          <Text bold>Couleurs</Text>
          <Text><Text color={BROWN}>■</Text> marron #8C5C41   <Text color="#573307">■</Text> marron foncé #573307   <Text color={GOLD}>■</Text> or (jamais de jaune)</Text>
          <Text bold>Polices</Text>
          <Text>Anton pour les titres · Poppins pour les textes</Text>
          <Text bold>Sous-titres</Text>
          <Text>un mot à la fois, Poppins blanc ombré noir, en minuscules</Text>
          <Text bold>Encarts</Text>
          <Text>pastille arrondie dorée, Poppins gras italique blanc ombré</Text>
          <Text bold>Règles</Text>
          <Text>son seulement quand un élément apparaît · vitesse normale de ma voix · vrais logos et vraies photos · zones sûres Instagram · un test avant la vidéo finale</Text>
          <Button key="charte-edit" onPress={() => void fill($, 'Modifie ma charte : ')}>✎ Modifier ma charte</Button>
        </Box>
      )
    }

    return (
      <Box flexDirection="column" paddingX={1}>
        {head}
        {body}
      </Box>
    )
  })
}
