import {combineReducers} from 'redux'
import "./userReducer"
import userInfoReducer from "./userReducer";
import friendsReducer from "./friendsReducer";

//all reducers combined
const rootReducer = combineReducers({
    user: userInfoReducer,
    friends:friendsReducer,
})


export default rootReducer;

// Map Redux state to React component props
export const mapAllStateToProps = (state) => {
    return {
        userId: state.user.userId,
        username: state.user.username,
        isInCall: state.user.isInCall
    };
};
