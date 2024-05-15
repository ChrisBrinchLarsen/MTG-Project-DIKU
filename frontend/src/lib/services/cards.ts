import { env } from '$env/dynamic/public'

export async function getCards() {
  const response = await fetch(`${env.PUBLIC_API_URL}/random-cards`, {
    method: 'GET',
    mode: 'cors'
  })

  const body = await response.json()

  return body
}

export async function guessCard(bodyMessage: object) {
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
