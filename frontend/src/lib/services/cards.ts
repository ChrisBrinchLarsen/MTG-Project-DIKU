import { env } from '$env/dynamic/public'

export async function getCards() {
  const response = await fetch(`${env.PUBLIC_API_URL}/random-cards`, {
    method: 'GET',
    mode: 'cors'
  })

  const body = await response.json()

  return body
}
