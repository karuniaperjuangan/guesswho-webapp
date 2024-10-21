
export interface Face {
    id: number;
    b64_face: string;
    img_url: string;
    name: string;
    description: string;
    detail_url: string;
    bbox: Bbox;
}

export interface Bbox {
    x_min: number; //ratio of x_min to image width
    y_min: number; //ratio of y_min to image height
    x_max: number; //ratio of x_max to image width
    y_max: number; //ratio of y_max to image height
}