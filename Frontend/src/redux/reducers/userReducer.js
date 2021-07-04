// Import all actions
import * as actions from '../actions/userActions'

//USER_DATA REDUCER

export const userInitialState = {
    userId: localStorage.getItem('userId'),
    username: localStorage.getItem('username'),
    isInCall: localStorage.getItem('isInCall')
};

export default function userInfoReducer(state = userInitialState, action) {
    switch (action.type){
        case actions.SET_USERID:
           localStorage. setItem('userId',action.payload);
            return {...state, userId:action.payload};
        case actions.SET_USERNAME:
            localStorage.setItem('username',action.payload);
            return {...state,username:action.payload};
        case actions.SET_IS_IN_CALL:
            localStorage.setItem('isInCall',action.payload);
            return {...state,isInCall:action.payload};
        default:
            return state
    }
}
