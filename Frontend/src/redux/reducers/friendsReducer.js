// Import all actions
import * as actions from '../actions/friendsActions'
import {findWithAttr} from "../../Utils";

export const friendsInitialState = {
    actList: [],
    rreqList: [],
    sreqList: [],
    decList: []
};

export default function friendsReducer(state = friendsInitialState, action) {
    let newList;
    let index;

    switch (action.type) {
        case actions.SET_LIST:
            switch (action.payload.list) {
                case "ACT": return {...state, actList: action.payload.friends};
                case "RREQ": return {...state, rreqList: action.payload.friends};
                case "SREQ": return {...state, sreqList: action.payload.friends};
                case "DEC": return {...state, decList: action.payload.friends};
                default:
                    return;
            }

        case actions.ADD_TO_LIST:
            switch (action.payload.list) {
                case "ACT":
                    newList=state.actList;
                    newList.push(action.payload.friend)
                    return {...state, actList:newList};
                case "RREQ":
                    newList=state.rreqList;
                    newList.push(action.payload.friend)
                    return {...state, rreqList:newList};
                case "SREQ":
                    newList=state.sreqList;
                    newList.push(action.payload.friend)
                    return {...state, sreqList:newList};
                case "DEC":
                    newList=state.decList;
                    newList.push(action.payload.friend)
                    return {...state, decList:newList};
                default:
                    return;
            }

        case actions.REMOVE_FROM_LIST:
            switch (action.payload.list) {
                case "ACT":
                    newList=state.actList;
                    index =  findWithAttr(newList,'name',action.payload.name)
                    if (index > -1) newList.splice(index, 1);
                    return {...state, actList:newList};
                case "RREQ":
                    newList=state.rreqList;
                    index =  findWithAttr(newList,'name',action.payload.name)
                    if (index > -1) newList.splice(index, 1);
                    return {...state, rreqList:newList};
                case "SREQ":
                    newList=state.sreqList;
                    index =  findWithAttr(newList,'name',action.payload.name)
                    if (index > -1) newList.splice(index, 1);
                    return {...state, sreqList:newList};
                case "DEC":
                    newList=state.decList;
                    index =  findWithAttr(newList,'name',action.payload.name)
                    if (index > -1) newList.splice(index, 1);
                    return {...state, decList:newList};
                default:
                    return;
            }
        default:
            return state
    }
}
