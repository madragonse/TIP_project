//redirects to login if user is not authenticated
import {Redirect, Route} from "react-router-dom";
import {connect} from "react-redux";


const PrivateRoute = ({ userId,component: Component, ...rest }) =>
{
    return (
        <Route {...rest} render={props => (
            userId!==null
                ? <Component {...props} />
                : <Redirect to={{ pathname: '/login', state: { from: props.location } }} />
        )} />
    );
}
// Map Redux state to React component props
const mapStateToProps = (state) => {
    return {
        userId: state.user.userId
    };
};
// Connect Redux to React
export default connect(mapStateToProps)(PrivateRoute)