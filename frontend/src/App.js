import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter } from "react-router-dom"

import Routes from './Routes'

const routerConfig = {
  basename: '/cabinet',
}

const App = () => {
  return (
    <BrowserRouter {...routerConfig} >
      <Routes />
    </BrowserRouter>
  )
}

export default App

ReactDOM.render(<App />, document.getElementById('app'));
