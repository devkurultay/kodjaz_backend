import React from 'react'
import ReactDOM from 'react-dom'
import { createStore, applyMiddleware } from 'redux'
import { Provider } from 'react-redux'
import thunk from 'redux-thunk'
import promise from 'redux-promise-middleware'
import { BrowserRouter } from "react-router-dom"

import cabinet from './reducers/reducers'

const store = createStore(
  cabinet,
  applyMiddleware(thunk, promise)
)

import Routes from './Routes'

const routerConfig = {
  basename: '/cabinet',
}

const App = () => {
  return (
    <Provider store={store}>
      <BrowserRouter {...routerConfig} >
        <Routes />
      </BrowserRouter>
    </Provider>
  )
}

export default App

ReactDOM.render(<App />, document.getElementById('app'));
