

export const formatTime = (timer) => {
    const getSeconds = `0${(timer % 60)}`.slice(-2)
    const minutes = `${Math.floor(timer / 60)}`
    const getMinutes = `0${minutes % 60}`.slice(-2)
    const getHours = `0${Math.floor(timer / 3600)}`.slice(-2)

    return `${getHours} : ${getMinutes} : ${getSeconds}`
}

//formats time without hours
export const formatTimeMinutes = (timer) => {
    const getSeconds = `0${(timer % 60)}`.slice(-2)
    const minutes = `${Math.floor(timer / 60)}`
    const getMinutes = `0${minutes % 60}`.slice(-2)

    return `${getMinutes} : ${getSeconds}`
}

export const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

//for adding multple classes on conditions to react elements
export function classNames(classes) {
    return Object.entries(classes)
        .filter(([key, value]) => value)
        .map(([key, value]) => key)
        .join(' ');
}

//finds index in array of object with given attribute
export function findWithAttr(array, attr, value) {
    for(var i = 0; i < array.length; i += 1) {
        if(array[i]['props'][attr] === value) {
            return i;
        }
    }
    return -1;
}

export function getCurrentTimestamp(){
    const currentDate = new Date();
    return currentDate.getTime();
}

export function hasNumber(string) {
    return /\d/.test(string);
}

export function hasUppercase(string) {
    return /[A-Z]/.test(string);
}

export function hasWhiteSpace(string) {
    return /[\s]/.test(string);
}