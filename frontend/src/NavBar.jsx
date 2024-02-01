import React, { useState } from 'react';
import LogoutButton from './LogoutButton';

const Navbar = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    return (
        <nav className="bg-red-500 text-white shadow-lg top-0 sticky">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <div className="flex items-center">
                        <img src="./logo.png" alt="Logo" className="h-10 w-10 mr-6 rounded-full"/>
                        <div className="flex-shrink-0">
                            <span className="font-semibold text-xl tracking-tight">UniMatch</span>
                        </div>
                        {/* Links for medium and larger screens */}
                        <div className="hidden md:flex">
                            <div className="ml-10 flex items-baseline space-x-4">
                                <a href="/matching" className="text-gray-300 hover:bg-red-400 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Matching</a>
                                <a href="/matches" className="text-gray-300 hover:bg-red-400 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Matches</a>
                                <a href="/profile" className="text-gray-300 hover:bg-red-400 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Profile</a>
                            </div>
                        </div>
                    </div>
                    {/* Logout for medium and larger screens */}
                    <div className='hidden md:flex items-center hover:bg-red-400 hover:text-white px-3 py-2 rounded-md text-sm font-medium'>
                        <LogoutButton />
                    </div>
                    {/* Menu button for small screens */}
                    <div className="md:hidden">
                        <button onClick={() => setIsMenuOpen(!isMenuOpen)} className="text-gray-300 hover:bg-red-400 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                            Menu
                        </button>
                    </div>
                </div>
                {/* Mobile menu, show/hide based on menu state */}
                {isMenuOpen && (
                    <div className="md:hidden">
                        <a href="/matching" className="text-gray-300 hover:bg-red-400 hover:text-white block px-3 py-2 rounded-md text-base font-medium">Matching</a>
                        <a href="/matches" className="text-gray-300 hover:bg-red-400 hover:text-white block px-3 py-2 rounded-md text-base font-medium">Matches</a>
                        <a href="/profile" className="text-gray-300 hover:bg-red-400 hover:text-white block px-3 py-2 rounded-md text-base font-medium">Profile</a>
                        <div className='hover:bg-red-400 hover:text-white px-3 py-2 rounded-md text-base font-medium'>
                            <LogoutButton />
                        </div>
                    </div>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
