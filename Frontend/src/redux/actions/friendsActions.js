// Create Redux action types
export const ADD_TO_LIST = 'ADD_TO_LIST'
export const REMOVE_FROM_LIST = 'REMOVE_FROM_LIST'
export const SET_LIST = 'SET_LIST'


export const addToFriendList = (friend,chosenList) => ({
    type: ADD_TO_LIST,
    payload: {
        'friend':friend,
        'list':chosenList
    },
})

export const removeFromFriendList = (name,chosenList) => ({
    type: REMOVE_FROM_LIST,
    payload: {
        'name':name,
        'list':chosenList
    },
})

export const setFriendList = (friends,chosenList) => ({
    type: SET_LIST,
    payload: {
        'friends':friends,
        'list':chosenList
    },
})


