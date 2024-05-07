import { env } from '$env/dynamic/public'

export async function getEmployees() {
  const response = await fetch(`${env.PUBLIC_API_URL}/employees`, {
    method: 'GET',
    mode: 'cors'
  })

  const body = await response.json()

  return body
}
