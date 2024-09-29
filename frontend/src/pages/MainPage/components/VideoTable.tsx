import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Routes } from "@/Router";
import { Badge } from "@/components/ui/badge";
import { useNavigate } from "react-router-dom";
import { VideoRepr } from "@/openapi/requests/types.gen";

type VideoTableProps = {
  data: VideoRepr[];
};

const VideoTable: React.FC<VideoTableProps> = ({ data }) => {
  const navigate = useNavigate();
  const onRowClick = (id: number) => {
    navigate(`${Routes.Video}/${id}`);
  };

  const croppedTags = (tags: string[] | null) => {
    if (!tags) return ''

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
        <TableHead>Статус</TableHead>
        <TableHead>Теги</TableHead>
      </TableHeader>
      <TableBody>
        {data.map((item) => (
          <TableRow key={`video-${item.id}`} onClick={() => onRowClick(item?.id)}>
            <TableCell className="max-w-48 w-max overflow-hidden text-ellipsis whitespace-nowrap font-medium">
              {item?.title}
            </TableCell>
            <TableCell className="max-w-40 overflow-hidden text-ellipsis whitespace-nowrap">
              <a
                href={item?.url}
                target="_blank"
                className="font-medium"
                onClick={(event) => {
                  event.stopPropagation();
                }}
              >
                {item?.url}
              </a>
            </TableCell>
            <TableCell className="w-max max-w-32">
              <Badge className="text-xs whitespace-nowrap" variant='default'>
                {item?.status}
              </Badge>
            </TableCell>
            <TableCell className="flex gap-2">
              {croppedTags(JSON.parse(item?.tags))}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default VideoTable;
