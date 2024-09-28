import React from "react";
// import {Home, LineChart, BookMarked, BookOpenCheck, Settings, ShoppingCart, Users2} from "lucide-react";
// import {Tooltip, TooltipContent, TooltipProvider, TooltipTrigger} from "~/components/ui/tooltip";
import {NavLink, Link} from "react-router-dom";
import {MenuItemsType} from "@/components/MainLayout/MainLayout.tsx";

type SidebarProps = {
    menuItems: MenuItemsType[];
};

const Sidebar: React.FC<SidebarProps> = ({menuItems}) => {
    return (
        <aside className="fixed inset-y-0 left-0 z-10 hidden w-56 flex-col bg-sidebar sm:flex">
            <nav className="flex flex-col items-start gap-2 px-2 sm:py-10">
                <Link
                    to="/"
                    className="
                        w-full text-white font-bold
                        text-3xl mb-5 cursor-pointer
                        flex justify-center items-center
                        transition-all duration-500 hover:opacity-80"
                >
                    <img src="/logo-light.svg" alt="VideoTags" className="h-8"/>
                    <span className="sr-only">VideoTags</span>
                </Link>
                {
                    menuItems.map((item, key) => (
                                    <NavLink
                                        key={`menu-item-${key}`}
                                        to={item.link}
                                        className="
                                            py-3 px-4 w-full text-sm
                                            flex flex-row items-center gap-2
                                            text-gray-500 rounded-md
                                            transition-all duration-500

                                            cursor-pointer hover:text-white
                                            aria-[current=page]:pointer-events-none
                                            aria-[current=page]:bg-white/10
                                            aria-[current=page]:text-white
                                        ">
                                        {item.icon}
                                        {item.text}
                                        <span className="sr-only">{item.text}</span>
                                    </NavLink>
                    ))
                }
            </nav>
        </aside>
    );
};

export default Sidebar;