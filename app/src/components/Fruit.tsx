import type { ReactElement, SyntheticEvent, KeyboardEvent } from "react";
import { useNavigate } from "react-router";

import type { IFruit } from "../types";
import { useMediaQuery } from "../utils/responsive";
import ImageAttribution from "./ImageAttribution";

const PREFERRED_IMAGE_WIDTH = 384;
const MOBILE_PADDING = 16;
const ASPECT_RATIO_WIDTH = 16;
const ASPECT_RATIO_HEIGHT = 9;
const IMAGE_INDEX_BELOW_THE_FOLD = 3;

export default function Fruit({
  fruit,
  index,
}: {
  fruit: IFruit;
  index: number;
}): ReactElement {
  const isTabletAndUp = useMediaQuery("(min-width: 600px)");
  const navigate = useNavigate();

  function onClick(event: SyntheticEvent<HTMLElement>): void {
    // Ignore if clicked element is an actual link (i.e. anchor tag)
    if ((event.target as HTMLElement).nodeName === "A") {
      return;
    }
    window.scrollTo(0, 0);
    navigate("/" + fruit.name.toLowerCase());
  }
  function onKeyDown(event: KeyboardEvent<HTMLElement>): void {
    if (event.key === "Enter") {
      onClick(event);
    }
  }

  const imageWidth = Math.min(
    PREFERRED_IMAGE_WIDTH,
    window.innerWidth - MOBILE_PADDING
  );
  const imageHeight = imageWidth / (ASPECT_RATIO_WIDTH / ASPECT_RATIO_HEIGHT);

  return (
    <div
      data-testid="FruitCard"
      className="select-none focus:outline-none focus:ring focus:ring-opacity-50 focus:ring-gray-500 focus:border-gray-300 cursor-pointer overflow-hidden shadow-lg dark:shadow-2xl rounded-lg"
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={onKeyDown}
    >
      <div className="relative">
        <img
          data-testid="FruitCardImage"
          loading={
            !isTabletAndUp && index >= IMAGE_INDEX_BELOW_THE_FOLD
              ? "lazy"
              : "eager"
          }
          decoding={
            !isTabletAndUp && index >= IMAGE_INDEX_BELOW_THE_FOLD
              ? "async"
              : "sync"
          }
          width={imageWidth}
          height={imageHeight}
          style={{
            backgroundColor: fruit.image.color,
          }}
          src={`${fruit.image.url}&w=${
            imageWidth * window.devicePixelRatio
          }&h=${imageHeight * window.devicePixelRatio}`}
          alt={fruit.name}
        />
        <ImageAttribution author={fruit.image.author} />
      </div>
      <h3 data-testid="FruitCardName" className="p-6 font-bold text-xl">
        {fruit.name}
      </h3>
    </div>
  );
}
