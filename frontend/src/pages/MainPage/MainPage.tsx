import React from 'react';
import EmptyView from "@/components/EmptyView";
import {Button} from "@/components/ui/button.tsx";
import {Plus} from "lucide-react";
import {useNavigate} from "react-router-dom";
import {Routes} from "@/Router.tsx";
import VideoTable from "@/pages/MainPage/components/VideoTable.tsx";

export type VideoDataItem = {
    name: string;
    tags: string[];
};

const MainPage: React.FC = () => {
    const navigate = useNavigate();

    const data = [{
        name: "test",
        tags: ["test1", "test 2"]
    },{
        name: "Cats cats video",
        tags: ["cats", "happy", "love"]
    }];

    return (
        <>
            <h2>Ваши видео</h2>
            {
                !data || !data.length
                ? (<EmptyView title="Список видео пуст">
                        <Button
                            className="flex gap-2"
                            onClick={() => navigate(Routes.New)}
                        >
                            <Plus className=""/>Добавить видео</Button>
                    </EmptyView>)
                : <VideoTable data={data}/>
            }
        </>
    );
};

export default MainPage;
