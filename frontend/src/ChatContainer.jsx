import React, {useEffect, useState, useRef} from 'react';
import Contact from './Contact';
import Message from './Message';
import { useAuth0 } from '@auth0/auth0-react';

const ChatContainer = () => {
    const { getIdTokenClaims } = useAuth0();
    const [idToken, setIdToken] = useState('');
    const [user, setUser] = useState('');

    useEffect(() => {
        const fetchIdToken = async () => {
            try {
                const idTokenClaims = await getIdTokenClaims();
                setIdToken(idTokenClaims.__raw);
            } catch (error) {
                console.error('Error getting ID token', error);
            }
        };

        fetchIdToken();
    }, [getIdTokenClaims]);

    useEffect(() => {
        fetch(`http://lissan.dev:8050/give-me-email?jwt=${idToken}`)
            .then(res => res.json())
            .then(res => setUser(res.email))
    }, [idToken])
    
    const [selected, setSelected] = useState(null);
    const [messages, setMessages] = useState([])
    const [currentMessage, setCurrentMessage] = useState('')
    const [contacts, setContacts] = useState([])

    useEffect(() => {
        if (user == '') return;
        fetch(`http://lissan.dev:8050/contact-list?user=${user}`)
            .then(res => res.json())
            .then(data => setContacts(data.contact_list))
    }, [user])

    useEffect(() => {
        if (selected == null || user == '') return;
        let receiver = contacts[selected][0]
        fetch(`http://lissan.dev:8050/messages?user=${user}&other=${receiver}`)
            .then(res => res.json())
            .then(data => setMessages(data.messages))
    }, [selected, user])

    const endOfListRef = useRef(null);
    const scrollToBottom = () => {
        endOfListRef.current?.scrollIntoView();
    };
    useEffect(scrollToBottom, [messages]);

    const handleSelect = (id) => {
        setSelected(id);
    }

    const handleChange = (e) => {
        setCurrentMessage(e.target.value)
    }
    
    const keyDown = (e) => {
        if (selected == null) return;
        if (e.key == "Enter") {
            let receiver = contacts[selected][0]
            fetch(`http://lissan.dev:8050/send-message?user=${user}&other=${receiver}&message=${currentMessage}`)
            setCurrentMessage('')
        }
    }

    return (
        <div className="flex mx-auto" style={{ height: `calc(100vh - 4rem)` }}>
            {/* Contacts Section */}
            <div className="w-1/4 bg-gray-200 overflow-y-auto">
                {contacts.length > 0 && (
                    contacts.map((contact, i) => {
                        return <Contact id={i} key={i} email={contact[0]} selected={selected === i} onSelect={handleSelect} name={contact[1]} pfp={"http://lissan.dev:8050/media/" + contact[2]} />
                    })
                )}
                {/* More contacts */}
            </div>

            {/* Chat Section */}
            <div className="w-3/4 bg-white p-4 flex flex-col">
                {/* Chat messages */}
                <div className="overflow-y-auto flex-grow">
                    
                    {messages.map((m, i) => {
                        return <Message key={i} text={m[1]} sender={m[2]} time={m[0]}/>
                    })}
                     <div ref={endOfListRef} />
                </div>

                {/* Message Input */}
                <div className="mt-4">
                    <input type="text" className="border p-2 w-full" placeholder="Type a message..." value={currentMessage} onChange={handleChange} onKeyDown={keyDown}/>
                </div>
            </div>
        </div>
    );
};

export default ChatContainer;