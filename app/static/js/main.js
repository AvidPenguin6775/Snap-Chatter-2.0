$(document).ready(function(){
	
	var $grid = $('.grid').masonry({
		gutter: 30
	});
	
	// layout Masonry after each image loads
	$grid.imagesLoaded().progress( function() {
		$grid.masonry('layout');
	});
	// if like heart is clicked 
	$('i.like').click(function(e) {
	
		e.stopPropagation();
		e.preventDefault();
		// update variables to change
		var like = $(this).hasClass('far');
		var image_id = $(this).data('image');
	  	var _this = $(this);
			// runs script to update image like from true to false.
		  $.getJSON(
			$SCRIPT_ROOT + '/like', 
			{
				like: like,
				image_id: image_id
			}, 
			function(result) {
				// if unliked remove unliked and add liked class
				if (like) {
					_this.removeClass('far');
					_this.addClass('fas');
				}else {
				// if liked remove liked and add unliked class
					_this.removeClass('fas');
					_this.addClass('far');
				}
			}
		);
	});
	// Pulls filter data and sets filter variable to image.
	if ($('#filter-select').length > 0 ) {
		var filter = $('#filter-select').data('filter');
		$('#filter-select').val(filter);
	}
	// Pulls category data and sets variable to image
	if ($('#category').length > 0 ) {
		var category = $('#category').data('category');
		$('#category').val(category);
	}
	// if image figure has changed remove old class and all the new filter.
	$('#filter-select').change(function(e) {
		var new_filter = 'filter-' + this.value;
		$('#image figure').removeClass();
		$('#image figure').addClass(new_filter);
	});
	
});

$('.grid-item figure').click(function(){
	//Fetch image data
	var image_data = $(this).closest('.grid-item').data(image);
	var image = image_data.image;

	//Build HTML from image data
	var description = `<p>${image.description}</p>`;
	var title = `<h5 class="modal-title">${image.name}<i class="fa fa-times" class="close" data-dismiss="modal" aria-label="Close" aria-hidden="true"></i></h5>`;
	var img = `<img src="${image.upload_location}" alt="${image.name}" />`;

	//Add to modal and open modal
	$('#image-modal .modal-body').html(img + title + description);
	$('.modal').modal('show');
});