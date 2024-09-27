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
        <aside className="fixed inset-y-0 left-0 z-10 hidden w-52 flex-col border-r bg-background sm:flex shadow-lg">
            <nav className="flex flex-col items-start gap-2 px-4 sm:py-8">
                <Link
                    to="/"
                    className="
                        w-full text-white font-bold
                        text-3xl pb-7 cursor-pointer
                        transition-all duration-500 hover:opacity-80"
                >
                    VIDEO TAGS
                    <span className="sr-only">VideoTags</span>
                </Link>
                {
                    menuItems.map((item, key) => (
                                    <NavLink
                                        key={`menu-item-${key}`}
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