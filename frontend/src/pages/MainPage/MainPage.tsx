import EmptyView from "@/components/EmptyView";
import { Button } from "@/components/ui/button.tsx";
import { Plus } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Routes } from "@/Router.tsx";
import VideoTable from "@/pages/MainPage/components/VideoTable.tsx";
import { useInferenceEndpointsServiceGetVideosV1VideosGet } from "@/openapi/queries";

const MainPage: React.FC = () => {
  const navigate = useNavigate();

  const { data } = useInferenceEndpointsServiceGetVideosV1VideosGet();

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
              <Plus className="" />Добавить видео</Button>
          </EmptyView>)
          : <VideoTable data={data} />
      }
    </>
  );
};

export default MainPage;
