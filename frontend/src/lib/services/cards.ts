import { env } from '$env/dynamic/public'
import type { Card, Guess, PartialCard } from '$lib/types/cards'

export async function initGame(): Promise<{ correctCard: PartialCard; cards: PartialCard[] }> {
  const response = await fetch(`${env.PUBLIC_API_URL}/init-game`, {
    method: 'GET',
    mode: 'cors'
  })

  const body = await response.json()

  return body
}

export async function guessCard(bodyMessage: {
  guessedCardId: number
  correctCardId: number
  cardIds: number[]
}): Promise<{ cards: PartialCard[]; guess: Guess }> {
  const response = await fetch(`${env.PUBLIC_API_URL}/guess`, {
    method: 'POST',
    mode: 'cors',
    body: JSON.stringify(bodyMessage),
    headers: {
      'Content-Type': 'application/json'
    }
  })

  const body = await response.json()

  return body
}

export async function getCard(bodyMessage: { cardId: string }): Promise<Card> {
  const response = await fetch(`${env.PUBLIC_API_URL}/get-card`, {
    method: 'POST',
    mode: 'cors',
    body: JSON.stringify(bodyMessage),
    headers: {
      'Content-Type': 'application/json'
    }
  })

  const body = await response.json()

  return body
}
