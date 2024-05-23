export type Card = {
  cardid: number
  name: string
  releasedate: string
  cmc: number
  oracle: string
  collectorid: string
  flavortext: string
  priceeur: number
  imagesmall: string
  imagenormal: string
  imagelarge: string
  setacro: string
  rarity: string
  artist: string
}

export type PartialCard = Pick<Card, 'cardid' | 'name' | 'cmc' | 'imagesmall'>

export const TRAITS_TO_GUESS = ['rarity', 'cmc', 'type'] as const

export type Guess = {
  [key in (typeof TRAITS_TO_GUESS)[number]]: {
    correctValues: string[]
    incorrectValues: string[]
  }
}
