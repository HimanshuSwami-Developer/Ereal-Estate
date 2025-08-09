// main.js - jQuery-based: hero hide + AJAX filter
(function($){
    // HERO hide/show
    const $hero = $('#hero');
    $(window).on('scroll', function(){
      if ($(this).scrollTop() > 120) {
        $hero.addClass('hero-hidden');
      } else {
        $hero.removeClass('hero-hidden');
      }
    });
  
    // Initialize filters
    window.initFilters = function(opts){
      const ajaxUrl = opts.ajaxUrl;
      const $results = $(opts.resultsContainer);
      const $meta = $(opts.metaContainer);
      const $form = $('#filter-form');
  
      function params(){
        return {
          q: $('#q').val(),
          location: $('#location').val(),
          min_price: $('#min_price').val(),
          max_price: $('#max_price').val()
        };
      }
  
      let timer = null;
      function fetchResults(){
        $.get(ajaxUrl, params())
          .done(function(data){
            $results.html(data.html);
            if ($meta.length) $meta.text(data.count + ' result(s)');
          })
          .fail(function(){ console.error('Filter request failed'); });
      }
  
      // debounce inputs
      $('#q, #location, #min_price, #max_price').on('input change', function(){
        clearTimeout(timer);
        timer = setTimeout(fetchResults, 300);
      });
  
      $('#reset-filters').on('click', function(){
        $form[0].reset();
        fetchResults();
      });
  
      // initial fetch
      fetchResults();
    };
  
  })(jQuery);
  