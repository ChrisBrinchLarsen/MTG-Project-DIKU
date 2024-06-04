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

export type PartialCard = Pick<Card, 'cardid' | 'name' | 'cmc' | 'imagesmall' | 'imagenormal'>

export type Guess = {
  [key in string]: {
    correctValues: (string | null)[]
    incorrectValues: (string | null)[]
    status: (string | null)
  }
}
