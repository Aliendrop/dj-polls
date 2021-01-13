export default (endpointName) => {
  const env = process.env.NODE_ENV
  // TODO: get from env
  const dev = 'http://localhost:8000/api/'
  const prod = dev  // FIXME:

  const api = {
    polls: 'polls',
    // ...
  }
  
  return (
    env === 'production' ?
      `${prod}${api[endpointName]}` :
      `${dev}${api[endpointName]}`
  )
}
