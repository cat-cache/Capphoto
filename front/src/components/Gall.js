import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import PhotoAlbum from "react-photo-album";
import Lightbox from "yet-another-react-lightbox";
import "yet-another-react-lightbox/styles.css";
import Fullscreen from "yet-another-react-lightbox/plugins/fullscreen";
import Slideshow from "yet-another-react-lightbox/plugins/slideshow";
import Thumbnails from "yet-another-react-lightbox/plugins/thumbnails";
import Zoom from "yet-another-react-lightbox/plugins/zoom";
import "yet-another-react-lightbox/plugins/thumbnails.css";

const Gall = ({ photos }) => {
  const [index, setIndex] = useState(-1);
  const [galleryPhotos, setGalleryPhotos] = useState([]);

  useEffect(() => {
    const loadPhotos = async () => {
      const loadedPhotos = [];

      for (let i = 0; i < photos.length; i++) {
        const path = photos[i];

        try {
          const img = new Image();
          img.src = path;
          await new Promise((resolve, reject) => {
            img.onload = () => resolve();
            img.onerror = (error) => reject(error);
          });

          const aspectRatio = img.naturalWidth / img.naturalHeight;
          loadedPhotos.push({
            src: path,
            width: 1080, // Initial width (adjust as needed)
            height: Math.round(1080 / aspectRatio),
          });
        } catch (error) {
          console.error("Error loading image:", error);
          // Handle error or skip problematic image
        }
      }

      setGalleryPhotos(loadedPhotos);
    };

    loadPhotos();
  }, [photos]);

  return (
    <>
      {galleryPhotos.length > 0 ? (
        <>
          <PhotoAlbum
            photos={galleryPhotos}
            layout="rows"
            targetRowHeight={150}
            onClick={({ index }) => setIndex(index)}
          />

          <Lightbox
            slides={galleryPhotos}
            open={index >= 0}
            index={index}
            close={() => setIndex(-1)}
            plugins={[Fullscreen, Slideshow, Thumbnails, Zoom]}
          />
        </>
      ) : (
        <div>Loading...</div>
      )}
    </>
  );
};

Gall.propTypes = {
  photos: PropTypes.arrayOf(PropTypes.string).isRequired,
};

export default Gall;
