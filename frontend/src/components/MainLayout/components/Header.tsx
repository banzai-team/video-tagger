import React from 'react';

import { BookOpenCheck, ChevronLeft } from 'lucide-react';
import {Button} from "@/components/ui/button.tsx";
import {Sheet, SheetClose, SheetContent, SheetTrigger} from "@/components/ui/sheet.tsx";
import {MenuItemsType} from "@/components/MainLayout/MainLayout.tsx";
import {Link, NavLink} from "react-router-dom";

type HeaderProps = {
    menuItems: MenuItemsType[];
};

const Header: React.FC<HeaderProps> = ({menuItems}) => {
    console.log(menuItems);
    return (
        <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-background px-4 sm:static sm:h-auto sm:border-0 sm:bg-transparent sm:px-6">
            <Sheet>
                <SheetTrigger asChild>
                    <Button size="icon" variant="light" className="sm:hidden">
                        <ChevronLeft className="h-5 w-5"/>
                        <span className="sr-only">Toggle Menu</span>
                    </Button>
                </SheetTrigger>
                <div className="text-white font-bold text-2xl sm:hidden">
                    VIDEO TAGS
                </div>
                <SheetContent side="left" className="sm:max-w-xs">
                    <nav className="grid gap-2 text-lg font-medium">
                        <SheetClose asChild>
                            <Link
                                to="/"
                                className="
                                    w-full text-white font-bold
                                    text-xl cursor-pointer pb-5
                                    transition-all duration-500 hover:opacity-80"
                            >
                                VIDEO TAGS
                                <span className="sr-only">VideoTags</span>
                            </Link>
                        </SheetClose>
                        {menuItems.map((item, key) => (
                            <SheetClose asChild>
                                <NavLink
                                    key={`mobile-menu-item-${key}`}
                                    to={item.link}
                                    className="
                                    py-3 px-2 w-full
                                    flex flex-row items-center gap-2
                                    text-white rounded-md
                                    transition-all duration-500

                                    cursor-pointer hover:bg-white/10
                                    aria-[current=page]:pointer-events-none
                                    aria-[current=page]:bg-white/20
                                    aria-[current=page]:text-blue-500
                                "
                                >
                                    {item.icon}
                                    {item.text}
                                </NavLink>
                            </SheetClose>
                        ))}
                    </nav>
                </SheetContent>
            </Sheet>
        </header>
    );
};

export default Header;
