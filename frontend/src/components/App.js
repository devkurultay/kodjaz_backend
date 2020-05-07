import React, { Component} from "react"
import { Switch, Route, Link } from "react-router-dom"

import Cabinet from './Cabinet.js'

const App = () => {
  return(
    <div className="site">
      Hello world! 
      <nav>
        <Link className={"nav-link"} to={"/cabinet/main/"}>Cabinet main page</Link>
        <Link className={"nav-link"} to={"/cabinet/create/"}>Create an exercise</Link>
      </nav>
      <Switch>
        <Route exact path={"/cabinet/create/"} component={Cabinet} />
        <Route exact path={"/cabinet/main/"} render={() => <div>Home again</div>} />
      </Switch>
    </div>
  )
}

export default App
