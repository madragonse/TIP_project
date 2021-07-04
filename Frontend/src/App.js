import ScrollToTop from "./components/Common/ScrollToTop";
import NavBar from "./components/Navigation/NavBar";
import LogRegScreen from "./components/LogReg/LogRegScreen";
import {Switch, Route, Redirect} from 'react-router-dom';
import {applyMiddleware, createStore} from "redux";
import rootReducer from "./redux/reducers/rootReducer";
import {composeWithDevTools} from "redux-devtools-extension";
import thunk from "redux-thunk";
import {Provider} from "react-redux";
import {BrowserRouter as Router} from 'react-router-dom';
import PrivateRoute from "./components/Common/PrivateRouter";
import MainPageScreen from "./components/MainPage/MainPageScreen";

//redux store
export const store = createStore(rootReducer, composeWithDevTools(applyMiddleware(thunk)))

function App() {
  return (
    <div className="App">
        <Provider store={store}>

            <Router>
                <ScrollToTop />
                <Route path="/" component={NavBar}/>
                <Switch>
                    <Route path="/login" component={LogRegScreen} />
                    <PrivateRoute path="/" component={MainPageScreen} />
                    <Redirect from="*" to="/" />
                </Switch>
            </Router>

        </Provider>
    </div>
  );
}
//TODO add  <NavBar/>npm au

export default App;
