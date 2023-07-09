let pieceImages = {
    r: "res/img/black_rook.png",
    n: "res/img/black_knight.png",
    b: "res/img/black_bishop.png",
    q: "res/img/black_queen.png",
    k: "res/img/black_king.png",
    p: "res/img/black_pawn.png",
    R: "res/img/white_rook.png",
    N: "res/img/white_knight.png",
    B: "res/img/white_bishop.png",
    Q: "res/img/white_queen.png",
    K: "res/img/white_king.png",
    P: "res/img/white_pawn.png",
};

function loadImage(src) {
    return new Promise(function (resolve, reject) {
        let img = new Image();
        img.onload = function () {
            resolve(img);
        };
        img.onerror = function () {
            reject(new Error("Failed to load image: " + src));
        };
        img.src = src;
    });
}

async function generateChessboard(fen, width, height) {
    let canvas = document.getElementById("chessboard");
    let ctx = canvas.getContext("2d");

    canvas.width = width;
    canvas.height = height;

    let squareWidth = width / 8;
    let squareHeight = height / 8;
    let borderWidth = squareHeight / 24;

    let ranks = fen.split("/");

    for (let rank = 0; rank < ranks.length; rank++) {
        let currentRank = ranks[rank];
        let fileIndex = 0;

        for (let file = 0; file < currentRank.length; file++) {
            let currentSquare = currentRank[file];

            if (!isNaN(currentSquare)) {
                let emptySquares = parseInt(currentSquare);
                for (let i = 0; i < emptySquares; i++) {
                    let x = fileIndex * squareWidth;
                    let y = rank * squareHeight;

                    // Draw the background color
                    ctx.fillStyle =
                        (fileIndex + rank) % 2 === 0 ? "#f0d9b5" : "#b58863";
                    ctx.fillRect(x, y, squareWidth, squareHeight);

                    // Draw the border
                    ctx.lineWidth = borderWidth;
                    ctx.strokeStyle = "#000000";
                    ctx.strokeRect(
                        x + borderWidth / 2,
                        y + borderWidth / 2,
                        squareWidth - borderWidth,
                        squareHeight - borderWidth
                    );

                    fileIndex++;
                }
            } else {
                let pieceImgSrc = pieceImages[currentSquare];
                let x = fileIndex * squareWidth;
                let y = rank * squareHeight;

                try {
                    let pieceImg = await loadImage(pieceImgSrc);

                    // Draw the background color
                    ctx.fillStyle =
                        (fileIndex + rank) % 2 === 0 ? "#f0d9b5" : "#b58863";
                    ctx.fillRect(x, y, squareWidth, squareHeight);

                    // Draw the border
                    ctx.lineWidth = borderWidth;
                    ctx.strokeStyle = "#000000";
                    ctx.strokeRect(
                        x + borderWidth / 2,
                        y + borderWidth / 2,
                        squareWidth - borderWidth,
                        squareHeight - borderWidth
                    );

                    // Draw the piece image
                    ctx.drawImage(pieceImg, x, y, squareWidth, squareHeight);

                    fileIndex++;
                } catch (error) {
                    console.error(error);
                }
            }
        }
    }
    // Add four green squares to the corners
  ctx.fillStyle = "#00FF00";
  ctx.fillRect(0, 0, squareWidth/5, squareHeight/5); // Top left corner
  ctx.fillRect(width - squareWidth/5, 0, squareWidth/5, squareHeight/5); // Top right corner
  ctx.fillRect(0, height - squareHeight/5, squareWidth/5, squareHeight/5); // Bottom left corner
  ctx.fillRect(width - squareWidth/5, height - squareHeight/5, squareWidth/5, squareHeight/5); // Bottom right corner
  canvas.style.border = `${borderWidth}px solid`;
}
