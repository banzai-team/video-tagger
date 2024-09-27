import { VideoDataItem } from "@/pages/MainPage/MainPage.tsx";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Routes } from "@/Router";
import { Badge } from "@/components/ui/badge";
import { useNavigate } from "react-router-dom";

type VideoTableProps = {
  data: VideoDataItem[];
};

const VideoTable: React.FC<VideoTableProps> = ({ data }) => {
  const navigate = useNavigate();
  const onRowClick = (id: string) => {
    navigate(`${Routes.Video}/${id}`);
  };

  const croppedTags = (tags: string[]) => {
    const items = tags.length > 3 ? tags.slice(0, 3) : tags
    const ellipsis = tags.length > 3 ? '...' : ''

    return <>
      {items.map(item => (
        <Badge className="text-xs whitespace-nowrap" variant='secondary'>
          {item}
        </Badge>)
      )}
      {ellipsis}
    </>
  }

  return (
    <Table>
      <TableHeader>
        <TableHead>Название</TableHead>
        <TableHead>Ссылка</TableHead>
        <TableHead>Теги</TableHead>
      </TableHeader>
      <TableBody>
        {data.map((item) => (
          <TableRow key={`video-${item.id}`} onClick={() => onRowClick(item.id)}>
            <TableCell className="max-w-48 w-max overflow-hidden text-ellipsis whitespace-nowrap font-medium">
              {item.name}
            </TableCell>
            <TableCell className="max-w-40 overflow-hidden text-ellipsis whitespace-nowrap">
              <a
                href={item.source}
                target="_blank"
                className="font-medium"
                onClick={(event) => {
                  event.stopPropagation();
                }}
              >
                {item.source}
              </a>
            </TableCell>
            <TableCell className="flex gap-2">
              {croppedTags(item.tags)}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default VideoTable;
