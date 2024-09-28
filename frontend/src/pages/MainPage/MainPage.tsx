import EmptyView from "@/components/EmptyView";
import {Button} from "@/components/ui/button.tsx";
import {Plus} from "lucide-react";
import {useNavigate} from "react-router-dom";
import {Routes} from "@/Router.tsx";
import VideoTable from "@/pages/MainPage/components/VideoTable.tsx";

export type VideoDataItem = {
    id: string;
    name: string;
    tags: string[];
    source: string;
};

const MainPage: React.FC = () => {
    const navigate = useNavigate();

    const data: VideoDataItem[] = [{
        id: '0',
        name: "test",
        tags: ["test1", "test 2", "test 3", "test 4"],
        source: 'https://rutube.ru/video/c6cc4d620b1d4338901770a44b3e82f4/'
    },{
        id: '1',
        name: "Cats cats video",
        tags: ["cats", "happy", "love"],
        source: 'https://rutube.ru/'
    }];

    return (
        <>
            <h2 className="mb-5">Ваши видео</h2>
            {
                !data || !data.length
                    ? (<EmptyView title="Список видео пуст">
                        <Button
                            className="flex gap-2"
                            onClick={() => navigate(Routes.New)}
                        >
                            <Plus className=""/>Добавить видео</Button>
                    </EmptyView>)
                    : <div><VideoTable data={data}/></div>
            }
        </>
    );
};

export default MainPage;
