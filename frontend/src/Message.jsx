import React from 'react';

const Message = (props) => {
    const messageStyle = props.sender ? 'text-right' : 'text-left';
    const messageColor = props.sender ? 'bg-blue-400 text-white' : 'bg-gray-300 text-black';

    return (
        <div className={`${messageStyle} my-4`}>
            <span className={`${messageColor} inline-block rounded-3xl bg-gray-300 py-3 px-5 max-w-lg break-words text-xl`}>
                {props.text}
            </span>
            <p className='text-sm mr-4'>{props.time}</p>
        </div>
    );
}

export default Message;
